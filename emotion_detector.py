import numpy as np
import librosa
import whisper
from scipy.signal import find_peaks
from moviepy import VideoFileClip


class EmotionDetector:
    """Detects emotional peaks in audio using volume analysis and transcription"""
    
    def __init__(self, sensitivity=0.6):
        """
        Initialize the emotion detector
        
        Args:
            sensitivity: Detection sensitivity (0.0 to 1.0)
        """
        self.sensitivity = sensitivity
        self.whisper_model = None
    
    def detect_peaks(self, audio_path, video_path=None):
        """
        Detect emotional peaks in audio using amplitude analysis
        
        Args:
            audio_path: Path to audio file
            video_path: Optional path to video for additional analysis
            
        Returns:
            List of peak timestamps with scores
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate RMS energy (loudness) over time
        hop_length = 512
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        
        # Calculate times for each frame
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        
        # Normalize RMS values
        rms_normalized = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-8)
        
        # Find peaks in RMS energy
        # Adjust threshold based on sensitivity
        threshold = 1.0 - self.sensitivity
        min_distance = int(sr / hop_length * 5)  # Minimum 5 seconds between peaks
        
        peaks, properties = find_peaks(
            rms_normalized,
            height=threshold,
            distance=min_distance,
            prominence=0.1
        )
        
        # Create peak list with timestamps and scores
        emotional_peaks = []
        for peak_idx in peaks:
            peak_time = times[peak_idx]
            peak_score = rms_normalized[peak_idx]
            
            emotional_peaks.append({
                'time': peak_time,
                'score': float(peak_score),
                'type': 'audio_peak'
            })
        
        # Sort by score (descending)
        emotional_peaks = sorted(emotional_peaks, key=lambda x: x['score'], reverse=True)
        
        return emotional_peaks
    
    def analyze_audio_features(self, audio_path):
        """
        Analyze additional audio features for emotion detection
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary of audio features over time
        """
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate various features
        hop_length = 512
        
        # Energy/Loudness
        rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        
        # Zero crossing rate (can indicate voice vs silence)
        zcr = librosa.feature.zero_crossing_rate(y, hop_length=hop_length)[0]
        
        # Spectral centroid (brightness of sound)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
        
        # Tempo/Beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        
        return {
            'times': times,
            'rms': rms,
            'zcr': zcr,
            'spectral_centroid': spectral_centroid,
            'tempo': tempo,
            'beat_frames': beat_frames
        }
    
    def transcribe_audio(self, audio_path, model_size='base'):
        """
        Transcribe audio using OpenAI Whisper
        
        Args:
            audio_path: Path to audio file
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
            
        Returns:
            Transcription with timestamps
        """
        try:
            # Load Whisper model (cached after first load)
            if self.whisper_model is None:
                print(f"Loading Whisper model ({model_size})...")
                self.whisper_model = whisper.load_model(model_size)
            
            # Transcribe
            result = self.whisper_model.transcribe(
                audio_path,
                word_timestamps=True,
                verbose=False
            )
            
            # Extract segments with timestamps
            segments = []
            for segment in result['segments']:
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })
            
            return {
                'text': result['text'],
                'segments': segments,
                'language': result.get('language', 'unknown')
            }
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return {
                'text': '',
                'segments': [],
                'language': 'unknown'
            }
    
    def find_keyword_moments(self, transcript, keywords):
        """
        Find moments in transcript containing specific keywords
        
        Args:
            transcript: Transcription result from transcribe_audio
            keywords: List of keywords to search for
            
        Returns:
            List of moments with keyword matches
        """
        keyword_moments = []
        
        if not transcript or not transcript.get('segments'):
            return keyword_moments
        
        for segment in transcript['segments']:
            text_lower = segment['text'].lower()
            
            # Check for keyword matches
            matched_keywords = [kw for kw in keywords if kw.lower() in text_lower]
            
            if matched_keywords:
                keyword_moments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'],
                    'keywords': matched_keywords,
                    'type': 'keyword_match'
                })
        
        return keyword_moments
    
    def combine_peaks_and_keywords(self, audio_peaks, keyword_moments, window=10):
        """
        Combine audio peaks and keyword moments to identify best clips
        
        Args:
            audio_peaks: List of audio peak moments
            keyword_moments: List of keyword match moments
            window: Time window (seconds) to consider peaks and keywords together
            
        Returns:
            Combined list of high-value moments
        """
        combined_moments = []
        
        # For each audio peak, check if there's a keyword nearby
        for peak in audio_peaks:
            peak_time = peak['time']
            score = peak['score']
            
            # Check for nearby keywords
            nearby_keywords = []
            for kw_moment in keyword_moments:
                if abs(kw_moment['start'] - peak_time) <= window:
                    nearby_keywords.extend(kw_moment['keywords'])
            
            combined_moments.append({
                'time': peak_time,
                'score': score,
                'keywords': list(set(nearby_keywords)),
                'has_keywords': len(nearby_keywords) > 0
            })
        
        # Boost scores for moments with keywords
        for moment in combined_moments:
            if moment['has_keywords']:
                moment['score'] *= 1.5  # Boost by 50%
        
        # Re-sort by adjusted score
        combined_moments = sorted(combined_moments, key=lambda x: x['score'], reverse=True)
        
        return combined_moments
