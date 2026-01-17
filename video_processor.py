import os
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip
import tempfile


class VideoProcessor:
    """Handles video file operations and basic processing"""
    
    def __init__(self, video_path):
        """
        Initialize the video processor
        
        Args:
            video_path: Path to the input video file
        """
        self.video_path = video_path
        self.video = None
        self.duration = 0
        self.fps = 0
        self.size = (0, 0)
        
        self._load_video()
    
    def _load_video(self):
        """Load video file and extract metadata"""
        try:
            self.video = VideoFileClip(self.video_path)
            self.duration = self.video.duration
            self.fps = self.video.fps
            self.size = self.video.size
        except Exception as e:
            raise Exception(f"Failed to load video: {str(e)}")
    
    def extract_audio(self, output_path=None):
        """
        Extract audio from video
        
        Args:
            output_path: Optional path for output audio file
            
        Returns:
            Path to extracted audio file
        """
        if output_path is None:
            # Create temp file for audio
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "extracted_audio.wav")
        
        try:
            audio = self.video.audio
            audio.write_audiofile(output_path, verbose=False, logger=None)
            return output_path
        except Exception as e:
            raise Exception(f"Failed to extract audio: {str(e)}")
    
    def get_video_info(self):
        """
        Get video metadata
        
        Returns:
            Dictionary with video information
        """
        return {
            'duration': self.duration,
            'fps': self.fps,
            'resolution': f"{self.size[0]}x{self.size[1]}",
            'width': self.size[0],
            'height': self.size[1]
        }
    
    def extract_subclip(self, start_time, end_time, output_path):
        """
        Extract a subclip from the video
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Path for output video file
            
        Returns:
            Path to the extracted clip
        """
        try:
            # Ensure times are within video duration
            start_time = max(0, start_time)
            end_time = min(self.duration, end_time)
            
            if start_time >= end_time:
                raise ValueError("Start time must be less than end time")
            
            # Extract subclip
            subclip = self.video.subclip(start_time, end_time)
            
            # Write to file
            subclip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            subclip.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to extract subclip: {str(e)}")
    
    def crop_to_vertical(self, clip, target_aspect_ratio=(9, 16)):
        """
        Crop video to vertical format
        
        Args:
            clip: MoviePy VideoFileClip object
            target_aspect_ratio: Tuple of (width, height) ratio
            
        Returns:
            Cropped VideoFileClip
        """
        from moviepy.video.fx.Crop import Crop
        
        # Calculate target dimensions
        video_width, video_height = clip.size
        target_width = int(video_height * target_aspect_ratio[0] / target_aspect_ratio[1])
        
        if target_width > video_width:
            # Video is already narrower than target
            return clip
        
        # Center crop
        x_center = video_width / 2
        x1 = x_center - target_width / 2
        x2 = x_center + target_width / 2
        
        return clip.with_effects([Crop(x1=int(x1), y1=0, x2=int(x2), y2=video_height)])
    
    def close(self):
        """Clean up resources"""
        if self.video:
            self.video.close()
    
    def __del__(self):
        """Destructor to ensure video is closed"""
        self.close()
