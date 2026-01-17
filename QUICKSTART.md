# 🚀 Quick Start Guide

## Option 1: One-Command Start (Recommended)

### Windows:
```bash
start.bat
```

### Mac/Linux:
```bash
chmod +x start.sh
./start.sh
```

This will automatically:
- Create virtual environment (if needed)
- Install all dependencies
- Start the Streamlit app
- Open your browser

## Option 2: Manual Start

### 1. Setup (First Time Only)
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run (Every Time)
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Start the app
streamlit run app.py
```

## First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] FFmpeg installed ([Download](https://ffmpeg.org/download.html))
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Gemini API key ([Get key](https://makersuite.google.com/app/apikey))

## Usage Steps

1. **Start the app** (see options above)
2. **Enter API key** in the sidebar
3. **Upload video** (or paste Google Drive link)
4. **Configure settings**:
   - Number of clips: 3-10
   - Clip duration: 15-90 seconds
   - Sensitivity: 0.1-1.0
5. **Click "Generate Clips"**
6. **Wait for processing** (progress bar shows status)
7. **Preview clips** in the output area
8. **Download clips** as MP4 files

## Test Your Installation

```bash
python test_installation.py
```

This will verify:
- ✅ All Python packages installed
- ✅ FFmpeg available
- ✅ Basic functionality working

## Common Issues & Fixes

### "streamlit: command not found"
```bash
pip install streamlit
```

### "FFmpeg not found"
```bash
# Windows (with Chocolatey)
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Slow processing
- Use smaller Whisper model (edit `emotion_detector.py`, line 58):
  ```python
  self.whisper_model = whisper.load_model("tiny")
  ```

## File Structure

```
PulsePointAI/
├── app.py                    # Main Streamlit app - START HERE
├── video_processor.py        # Video handling
├── emotion_detector.py       # Audio analysis & transcription
├── clip_generator.py         # AI-powered clip creation
├── utils.py                  # Helper functions
├── requirements.txt          # Python dependencies
├── test_installation.py      # Installation tester
├── start.bat                 # Windows quick start
├── start.sh                  # Mac/Linux quick start
├── README.md                 # Full documentation
├── INSTALLATION.md           # Detailed install guide
├── PROJECT_OVERVIEW.md       # Technical overview
└── .env.example              # Environment variables template
```

## Getting Help

1. **Installation issues**: See [INSTALLATION.md](INSTALLATION.md)
2. **Usage questions**: See [README.md](README.md)
3. **Technical details**: See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
4. **Bugs**: Open an issue on GitHub

## Pro Tips

💡 **Faster Processing**: Use "base" or "tiny" Whisper model
💡 **Better Results**: Increase sensitivity for quieter videos
💡 **Vertical Format**: Enable "Smart Crop" for TikTok/Reels
💡 **Engagement**: Enable "Dynamic Captions" for hooks
💡 **Batch Work**: Process multiple videos by restarting after each

## Next Steps

After successful setup:
1. Test with the provided sample video
2. Try with your own content
3. Experiment with different settings
4. Share your generated clips!

---

**Need help?** Check the documentation files or open an issue on GitHub.
