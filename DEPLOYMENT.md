# Deploying PulsePoint AI to Streamlit Community Cloud

## Quick Deployment Steps

### 1. Prerequisites
- GitHub account
- Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `Sankalpps/pulsepointai`
4. Set the main file path: `app.py`
5. Click "Advanced settings"
6. Add your secrets in the "Secrets" section:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```
7. Click "Deploy!"

### 3. Important Notes

- **DO NOT commit your `.env` file** - it's already in `.gitignore`
- **Add secrets via Streamlit Cloud dashboard** - never commit API keys
- The app will automatically install dependencies from `requirements.txt`
- Make sure FFmpeg is available (Streamlit Cloud includes it by default)

### 4. Local Development

For local development, use your `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

### 5. Troubleshooting

If deployment fails:
- Check that all dependencies in `requirements.txt` are compatible
- Verify your Gemini API key is valid
- Check Streamlit Cloud logs for specific errors
- Ensure FFmpeg-dependent features work in the cloud environment

## Repository Structure
```
PulsePointAI/
├── app.py                 # Main Streamlit application
├── video_processor.py     # Video processing logic
├── emotion_detector.py    # Emotion detection
├── clip_generator.py      # Clip generation
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── .env                 # Local environment variables (NOT committed)
└── .streamlit/
    └── secrets.toml     # Local secrets template (NOT committed)
```

## Support

For issues or questions:
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Review the [Streamlit Community Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)
