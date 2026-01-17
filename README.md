# PulsePoint AI 🎬

**Transform long-form videos into viral short clips using AI**

PulsePoint AI automatically identifies emotional peaks, transcribes content, and uses Google Gemini AI to extract the most engaging moments from your long-form videos, turning them into ready-to-post social media clips.

## 🎯 Features

- **🎵 Emotional Peak Detection**: Uses audio analysis to find high-energy moments
- **📝 AI-Powered Transcription**: Transcribes video content with OpenAI Whisper
- **🤖 Smart Moment Selection**: Google Gemini AI identifies the most viral-worthy content
- **✂️ Automated Clip Generation**: Creates 3-10 short clips (15-90 seconds each)
- **📱 Vertical Format Support**: Optional smart-crop to 9:16 for TikTok/Reels/Shorts
- **💬 Dynamic Captions**: Optional text overlays for better engagement

## 🚀 Demo Video

[Watch the demo video here](#)

**Sample Output Clips:**
- [Clip 1 - Sample Output](outputs/clip_1.mp4)
- [Clip 2 - Sample Output](outputs/clip_2.mp4)
- [Clip 3 - Sample Output](outputs/clip_3.mp4)

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- FFmpeg installed on your system ([Download here](https://ffmpeg.org/download.html))

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/PulsePointAI.git
cd PulsePointAI
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

**Activate the virtual environment:**
- Windows: `.venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the App

1. **Enter API Key**: Paste your Google Gemini API key in the sidebar
2. **Configure Settings**:
   - Number of clips (3-10)
   - Clip duration (15-90 seconds)
   - Emotion detection sensitivity
   - Enable optional features (smart crop, captions)
3. **Upload Video**: 
   - Upload a video file (MP4, MOV, AVI, MKV)
   - Or provide a Google Drive link
4. **Generate Clips**: Click "Generate Clips" and wait for processing
5. **Download Results**: Preview and download generated clips

## 📁 Project Structure

```
PulsePointAI/
├── app.py                  # Main Streamlit application
├── video_processor.py      # Video processing utilities
├── emotion_detector.py     # Audio analysis and transcription
├── clip_generator.py       # AI-powered clip generation
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔑 Environment Variables

Create a `.env` file (optional) for storing your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Video Processing**: MoviePy, OpenCV
- **Audio Analysis**: Librosa
- **Transcription**: OpenAI Whisper
- **AI Analysis**: Google Gemini 1.5 Flash
- **Face Detection**: MediaPipe (optional)

## 📊 How It Works

1. **Video Upload**: User uploads a long-form video
2. **Audio Extraction**: Extract audio track from video
3. **Emotion Detection**: Analyze audio for high-energy moments using:
   - RMS energy (loudness)
   - Spectral features
   - Peak detection algorithms
4. **Transcription**: Convert speech to text with timestamps using Whisper
5. **AI Analysis**: Send transcript + emotional peaks to Google Gemini to identify:
   - Most engaging moments
   - Viral-worthy content
   - Self-contained segments
6. **Clip Generation**: Extract and process selected moments:
   - Cut video segments
   - Optional: Crop to vertical format
   - Optional: Add captions
7. **Output**: Provide downloadable MP4 clips ready for social media

## 🎯 Use Cases

- **Content Creators**: Turn podcast episodes into social media content
- **Educators**: Extract key teaching moments from lectures
- **Coaches/Mentors**: Create promotional clips from webinars
- **Marketers**: Generate testimonial snippets from long interviews

## ⚙️ Configuration Options

### Emotion Detection Sensitivity
- **Low (0.1-0.3)**: Only detect very high-energy moments
- **Medium (0.4-0.7)**: Balanced detection (recommended)
- **High (0.8-1.0)**: Detect more subtle peaks

### Clip Duration
- **15-30s**: TikTok-style quick hits
- **30-60s**: Instagram Reels
- **60-90s**: YouTube Shorts

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# Windows (using Chocolatey)
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### CUDA/GPU Issues
If you have GPU issues with Whisper, use CPU mode by editing `emotion_detector.py`:
```python
whisper.load_model(model_size, device="cpu")
```

### Memory Issues
For large videos, reduce Whisper model size in `emotion_detector.py`:
```python
self.whisper_model = whisper.load_model("tiny")  # or "base"
```

## 📝 Sample Test Video

Test the application using the provided sample video:
[Input video for ByteSize Hackathon.mp4](https://drive.google.com/your-test-video-link)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 👥 Authors

- Your Name - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- Google Gemini for powerful AI analysis
- OpenAI Whisper for accurate transcription
- MoviePy for video processing
- Streamlit for the amazing web framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: your.email@example.com

---

**Built for [ByteSize Hackathon Name]** 🚀

Made with ❤️ using Python, AI, and lots of coffee ☕
