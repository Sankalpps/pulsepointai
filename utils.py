"""
Utility functions for PulsePoint AI
"""
import os
import re
from urllib.parse import urlparse, parse_qs
import requests


def is_valid_video_file(filename):
    """
    Check if file is a valid video format
    
    Args:
        filename: Name of the file
        
    Returns:
        Boolean indicating if file is valid
    """
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def extract_google_drive_id(url):
    """
    Extract file ID from Google Drive URL
    
    Args:
        url: Google Drive URL
        
    Returns:
        File ID or None
    """
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)',
        r'/open\?id=([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def download_google_drive_file(file_id, output_path):
    """
    Download file from Google Drive
    
    Args:
        file_id: Google Drive file ID
        output_path: Path to save downloaded file
        
    Returns:
        Path to downloaded file or None on error
    """
    try:
        # Google Drive direct download URL
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        session = requests.Session()
        response = session.get(url, stream=True)
        
        # Handle large file confirmation
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
                response = session.get(url, stream=True)
                break
        
        # Download file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
        
        return output_path
        
    except Exception as e:
        print(f"Error downloading from Google Drive: {str(e)}")
        return None


def format_time(seconds):
    """
    Format seconds into MM:SS or HH:MM:SS
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def estimate_processing_time(video_duration, num_clips):
    """
    Estimate processing time based on video duration
    
    Args:
        video_duration: Duration of video in seconds
        num_clips: Number of clips to generate
        
    Returns:
        Estimated time in seconds
    """
    # Rough estimates:
    # - Audio extraction: 5% of video duration
    # - Transcription: 10% of video duration
    # - AI analysis: 30 seconds base + 2 seconds per clip
    # - Clip generation: 5 seconds per clip
    
    extraction_time = video_duration * 0.05
    transcription_time = video_duration * 0.10
    ai_time = 30 + (num_clips * 2)
    generation_time = num_clips * 5
    
    total = extraction_time + transcription_time + ai_time + generation_time
    
    return int(total)


def validate_api_key(api_key):
    """
    Basic validation of API key format
    
    Args:
        api_key: API key string
        
    Returns:
        Boolean indicating if format is valid
    """
    if not api_key or len(api_key) < 20:
        return False
    
    # Google API keys typically start with certain patterns
    # This is a basic check
    return True


def get_file_size_mb(file_path):
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


def cleanup_temp_files(directory):
    """
    Clean up temporary files in directory
    
    Args:
        directory: Directory to clean
    """
    import shutil
    
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            os.makedirs(directory)
        except Exception as e:
            print(f"Error cleaning up temp files: {str(e)}")
