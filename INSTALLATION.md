# Installation Guide for PulsePoint AI

## Quick Start (5 minutes)

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Install FFmpeg
FFmpeg is required for video processing:

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Step 3: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/PulsePointAI.git
cd PulsePointAI

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### Step 5: Verify Installation
```bash
python test_installation.py
```

### Step 6: Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Troubleshooting

### Issue: "FFmpeg not found"
**Solution:** Make sure FFmpeg is in your system PATH. After installation, restart your terminal.

### Issue: "CUDA out of memory" during transcription
**Solution:** Edit `emotion_detector.py` and change:
```python
self.whisper_model = whisper.load_model("tiny")  # Use smaller model
```

### Issue: Slow processing
**Solutions:**
- Use smaller Whisper model ("tiny" or "base")
- Reduce number of clips
- Reduce clip duration
- Close other applications

### Issue: "Invalid API key"
**Solution:** 
- Make sure you copied the complete API key
- Check for extra spaces
- Generate a new key from Google AI Studio

### Issue: Import errors
**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

## System Requirements

### Minimum:
- Python 3.8+
- 4 GB RAM
- 2 GB free disk space
- Internet connection

### Recommended:
- Python 3.10+
- 8 GB RAM
- 5 GB free disk space
- GPU (optional, for faster processing)

## Dependencies Explained

- **Streamlit**: Web interface
- **MoviePy**: Video editing and processing
- **OpenCV**: Computer vision operations
- **Librosa**: Audio analysis
- **OpenAI Whisper**: Speech-to-text transcription
- **Google Generative AI**: Content analysis with Gemini
- **MediaPipe**: Face detection (optional feature)
- **NumPy/SciPy**: Numerical computations

## Next Steps

After installation:
1. Run the app: `streamlit run app.py`
2. Enter your Gemini API key in the sidebar
3. Upload a test video
4. Adjust settings as needed
5. Click "Generate Clips"

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Run `python test_installation.py` to verify your setup
- Open an issue on GitHub for bugs
- Email support for other questions

## Optional: Environment Variables

Create a `.env` file for persistent settings:
```bash
cp .env.example .env
# Edit .env and add your API key
```

Then modify `app.py` to load from .env:
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```
