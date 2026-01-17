import os
import tempfile
from pathlib import Path
import google.generativeai as genai
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import cv2
import mediapipe as mp


class ClipGenerator:
    """Generates short clips from long-form video using AI analysis"""
    
    def __init__(self, gemini_api_key):
        """
        Initialize the clip generator
        
        Args:
            gemini_api_key: Google Gemini API key
        """
        self.api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # MediaPipe for face detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = None
    
    def identify_key_moments(self, transcript, emotional_peaks, num_clips=5, clip_duration=60):
        """
        Use Gemini AI to identify the most valuable moments for clips
        
        Args:
            transcript: Video transcript with timestamps
            emotional_peaks: List of emotional peak moments
            num_clips: Number of clips to generate
            clip_duration: Target duration for each clip
            
        Returns:
            List of key moments with start/end times and metadata
        """
        # Prepare prompt for Gemini
        transcript_text = transcript.get('text', '') if transcript else ''
        segments = transcript.get('segments', []) if transcript else []
        
        # Create a summary of emotional peaks
        peaks_summary = "\n".join([
            f"Peak at {peak['time']:.1f}s (score: {peak['score']:.2f})"
            for peak in emotional_peaks[:20]  # Top 20 peaks
        ])
        
        # Create prompt
        prompt = f"""You are an expert video editor analyzing a long-form video to extract the most viral-worthy, high-impact short clips.

VIDEO TRANSCRIPT:
{transcript_text[:8000]}  # Limit to avoid token limits

EMOTIONAL PEAKS (high energy moments):
{peaks_summary}

TASK:
Identify the {num_clips} best moments from this video that would make engaging {clip_duration}-second social media clips (TikTok/Reels/Shorts).

CRITERIA:
- Look for moments with strong emotional impact, surprising insights, or actionable advice
- Prefer segments near the identified emotional peaks
- Each clip should be self-contained and make sense out of context
- Look for "hook" moments that grab attention in first 3 seconds
- Prioritize controversial, funny, or profound statements

OUTPUT FORMAT:
Return exactly {num_clips} moments in this JSON format:
[
  {{
    "start_time": <seconds>,
    "end_time": <seconds>,
    "title": "<catchy 5-8 word title>",
    "hook": "<attention-grabbing first line>",
    "reason": "<why this moment is valuable>",
    "estimated_virality": <score 1-10>
  }}
]

IMPORTANT: 
- Make sure start_time and end_time are actual numbers (floats)
- Each clip should be approximately {clip_duration} seconds long
- Clips should not overlap
- Return ONLY the JSON array, no other text
"""
        
        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            import json
            import re
            
            # Try to find JSON array in response
            json_match = re.search(r'\[\s*\{.*\}\s*\]', response_text, re.DOTALL)
            
            if json_match:
                moments_data = json.loads(json_match.group())
            else:
                # Fallback: create moments from emotional peaks
                moments_data = self._create_fallback_moments(
                    emotional_peaks,
                    num_clips,
                    clip_duration
                )
            
            # Validate and adjust moments
            validated_moments = self._validate_moments(moments_data, clip_duration)
            
            return validated_moments
            
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            # Fallback to peak-based selection
            return self._create_fallback_moments(emotional_peaks, num_clips, clip_duration)
    
    def _create_fallback_moments(self, emotional_peaks, num_clips, clip_duration):
        """
        Create moments based on emotional peaks when AI fails
        
        Args:
            emotional_peaks: List of emotional peaks
            num_clips: Number of clips to create
            clip_duration: Duration of each clip
            
        Returns:
            List of moment dictionaries
        """
        moments = []
        
        for i, peak in enumerate(emotional_peaks[:num_clips]):
            peak_time = peak['time']
            
            # Center the clip around the peak
            start_time = max(0, peak_time - clip_duration / 2)
            end_time = start_time + clip_duration
            
            moments.append({
                'start_time': start_time,
                'end_time': end_time,
                'title': f'High Energy Moment {i + 1}',
                'hook': 'Watch this powerful moment',
                'reason': f'Emotional peak detected (score: {peak["score"]:.2f})',
                'estimated_virality': int(peak['score'] * 10),
                'score': peak['score']
            })
        
        return moments
    
    def _validate_moments(self, moments, clip_duration):
        """
        Validate and adjust moment timings
        
        Args:
            moments: List of moment dictionaries
            clip_duration: Target clip duration
            
        Returns:
            Validated list of moments
        """
        validated = []
        
        for moment in moments:
            # Ensure required fields exist
            if 'start_time' not in moment or 'end_time' not in moment:
                continue
            
            start = float(moment['start_time'])
            end = float(moment['end_time'])
            
            # Adjust if duration is off
            if end - start != clip_duration:
                end = start + clip_duration
            
            validated.append({
                'start_time': start,
                'end_time': end,
                'title': moment.get('title', 'Clip'),
                'hook': moment.get('hook', ''),
                'reason': moment.get('reason', ''),
                'score': moment.get('estimated_virality', 5) / 10.0
            })
        
        return validated
    
    def create_clip(self, video_path, moment, clip_index, smart_crop=False, add_captions=False):
        """
        Create a video clip from a moment
        
        Args:
            video_path: Path to source video
            moment: Moment dictionary with start/end times
            clip_index: Index of this clip
            smart_crop: Whether to crop to vertical format
            add_captions: Whether to add captions
            
        Returns:
            Path to generated clip
        """
        # Create output directory
        output_dir = Path(tempfile.gettempdir()) / "pulsepoint_clips"
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / f"clip_{clip_index + 1}.mp4"
        
        try:
            # Load video
            video = VideoFileClip(video_path)
            
            # Extract subclip
            start_time = moment['start_time']
            end_time = min(moment['end_time'], video.duration)
            
            clip = video.subclip(start_time, end_time)
            
            # Smart crop to vertical if enabled
            if smart_crop:
                clip = self._crop_to_vertical_centered(clip)
            
            # Add captions if enabled
            if add_captions and moment.get('hook'):
                clip = self._add_caption_overlay(clip, moment['hook'])
            
            # Write output
            clip.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None,
                fps=24
            )
            
            # Cleanup
            clip.close()
            video.close()
            
            return str(output_path)
            
        except Exception as e:
            print(f"Error creating clip: {str(e)}")
            raise
    
    def _crop_to_vertical_centered(self, clip):
        """
        Crop video to vertical (9:16) format, centered on content
        
        Args:
            clip: MoviePy VideoFileClip
            
        Returns:
            Cropped clip
        """
        from moviepy.video.fx.Crop import Crop
        
        width, height = clip.size
        target_width = int(height * 9 / 16)
        
        if target_width >= width:
            # Already narrow enough
            return clip
        
        # Center crop
        x_center = width / 2
        x1 = x_center - target_width / 2
        x2 = x_center + target_width / 2
        
        return clip.with_effects([Crop(x1=int(x1), y1=0, x2=int(x2), y2=height)])
    
    def _add_caption_overlay(self, clip, text):
        """
        Add text caption overlay to video
        
        Args:
            clip: MoviePy VideoFileClip
            text: Caption text
            
        Returns:
            Clip with caption overlay
        """
        try:
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=40,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2,
                method='caption',
                size=(clip.w * 0.9, None)
            )
            
            # Position at bottom
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration)
            
            # Composite
            final_clip = CompositeVideoClip([clip, txt_clip])
            
            return final_clip
            
        except Exception as e:
            print(f"Error adding caption: {str(e)}")
            return clip  # Return original if captioning fails
