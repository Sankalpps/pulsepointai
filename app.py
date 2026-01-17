import streamlit as st
import os
from pathlib import Path
import tempfile
from video_processor import VideoProcessor
from emotion_detector import EmotionDetector
from clip_generator import ClipGenerator
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# Page configuration
st.set_page_config(
    page_title="PulsePoint AI",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-size: 18px;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .output-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🎬 PulsePoint AI</h1>
        <p>Transform long-form videos into viral short clips</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'output_clips' not in st.session_state:
    st.session_state.output_clips = []

def main():
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        gemini_api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )
        
        # Processing options
        st.subheader("Processing Options")
        num_clips = st.slider("Number of clips to generate", 3, 10, 5)
        clip_duration = st.slider("Clip duration (seconds)", 15, 90, 60)
        
        # Optional features
        st.subheader("Optional Features")
        enable_smart_crop = st.checkbox("Smart Crop to Vertical (9:16)", value=False)
        enable_captions = st.checkbox("Generate Dynamic Captions", value=False)
        
        # Audio sensitivity
        sensitivity = st.slider(
            "Emotion Detection Sensitivity",
            0.1, 1.0, 0.6,
            help="Higher values detect more emotional peaks"
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Video")
        
        # Video input options
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Google Drive Link"]
        )
        
        video_file = None
        video_path = None
        drive_link = None
        
        if input_method == "Upload File":
            video_file = st.file_uploader(
                "Upload your long-form video",
                type=['mp4', 'mov', 'avi', 'mkv']
            )
            
            if video_file:
                # Save uploaded file to temp directory
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(video_file.read())
                    video_path = tmp_file.name
                
                st.success(f"✅ Video uploaded: {video_file.name}")
                
                # Display video preview
                st.video(video_file)
        
        else:
            drive_link = st.text_input("Enter Google Drive link")
            if drive_link:
                st.info("📥 Google Drive download will be implemented")
                # TODO: Implement Google Drive download
        
        # Process button
        if st.button("🚀 Generate Clips", disabled=not video_path and not drive_link):
            if not gemini_api_key:
                st.error("⚠️ Please enter your Google Gemini API key in the sidebar")
            else:
                process_video(
                    video_path,
                    gemini_api_key,
                    num_clips,
                    clip_duration,
                    sensitivity,
                    enable_smart_crop,
                    enable_captions
                )
    
    with col2:
        st.header("🎥 Generated Clips")
        
        if st.session_state.processing_complete and st.session_state.output_clips:
            st.success(f"✅ Generated {len(st.session_state.output_clips)} clips!")
            
            for idx, clip_info in enumerate(st.session_state.output_clips):
                with st.expander(f"Clip {idx + 1}: {clip_info['title']}", expanded=True):
                    st.markdown(f"**Time Range:** {clip_info['start_time']:.1f}s - {clip_info['end_time']:.1f}s")
                    st.markdown(f"**Emotion Score:** {clip_info['score']:.2f}")
                    
                    if os.path.exists(clip_info['path']):
                        st.video(clip_info['path'])
                        
                        # Download button
                        with open(clip_info['path'], 'rb') as f:
                            st.download_button(
                                label=f"⬇️ Download Clip {idx + 1}",
                                data=f,
                                file_name=f"clip_{idx + 1}.mp4",
                                mime="video/mp4"
                            )
                    else:
                        st.error("Clip file not found")
        
        elif st.session_state.processing_complete:
            st.warning("No clips were generated. Try adjusting the sensitivity settings.")
        
        else:
            st.info("👈 Upload a video and click 'Generate Clips' to get started")


def process_video(video_path, api_key, num_clips, clip_duration, sensitivity, smart_crop, captions):
    """Process the video and generate clips"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Initialize processors
        status_text.text("🔧 Initializing processors...")
        progress_bar.progress(10)
        
        video_processor = VideoProcessor(video_path)
        emotion_detector = EmotionDetector(sensitivity=sensitivity)
        clip_generator = ClipGenerator(api_key)
        
        # Step 2: Extract audio and analyze
        status_text.text("🎵 Analyzing audio for emotional peaks...")
        progress_bar.progress(25)
        
        audio_path = video_processor.extract_audio()
        emotional_peaks = emotion_detector.detect_peaks(audio_path, video_path)
        
        # Step 3: Transcribe video
        status_text.text("📝 Transcribing video content...")
        progress_bar.progress(40)
        
        transcript = emotion_detector.transcribe_audio(audio_path)
        
        # Step 4: Use Gemini to identify best moments
        status_text.text("🤖 Using AI to identify key moments...")
        progress_bar.progress(55)
        
        best_moments = clip_generator.identify_key_moments(
            transcript,
            emotional_peaks,
            num_clips,
            clip_duration
        )
        
        # Step 5: Generate clips
        status_text.text("✂️ Generating video clips...")
        progress_bar.progress(70)
        
        output_clips = []
        for idx, moment in enumerate(best_moments):
            clip_path = clip_generator.create_clip(
                video_path,
                moment,
                idx,
                smart_crop=smart_crop,
                add_captions=captions
            )
            
            output_clips.append({
                'path': clip_path,
                'title': moment.get('title', f'Clip {idx + 1}'),
                'start_time': moment['start_time'],
                'end_time': moment['end_time'],
                'score': moment.get('score', 0.0)
            })
            
            progress_bar.progress(70 + (idx + 1) * (30 // len(best_moments)))
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Processing complete!")
        
        st.session_state.output_clips = output_clips
        st.session_state.processing_complete = True
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        status_text.text("Processing failed")
        progress_bar.empty()


if __name__ == "__main__":
    main()
