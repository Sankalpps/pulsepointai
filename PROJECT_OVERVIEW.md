# PulsePoint AI - Project Overview

## 🎯 Problem Statement

Mentors, educators, and content creators produce hours of high-value, long-form video content (lectures, podcasts, workshops), but modern audiences consume information in 60-second bursts. Valuable insights are buried in 60-minute videos, making them inaccessible to average viewers.

## 💡 Solution

**PulsePoint AI** is an automated video processing platform that uses AI and multimodal models to:
1. Identify "Emotional Peaks" - high-energy or profound moments using audio analysis
2. Transcribe and understand content using AI
3. Generate 3-5 viral-worthy short clips from long-form videos
4. (Optional) Smart-crop to vertical format for social media
5. (Optional) Add dynamic captions for engagement

## 🏗️ Architecture

### Core Components

1. **app.py** - Main Streamlit web interface
   - User-friendly UI for video upload
   - Configuration options (clip count, duration, sensitivity)
   - Real-time processing feedback
   - Preview and download generated clips

2. **video_processor.py** - Video handling module
   - Load and validate video files
   - Extract audio tracks
   - Generate subclips with precise timing
   - Optional vertical cropping (9:16 aspect ratio)

3. **emotion_detector.py** - Audio analysis engine
   - RMS energy analysis to detect loudness peaks
   - Spectral analysis for audio features
   - OpenAI Whisper integration for transcription
   - Peak detection algorithms with configurable sensitivity

4. **clip_generator.py** - AI-powered clip creation
   - Google Gemini 1.5 Flash integration
   - Intelligent moment selection based on:
     - Emotional peaks from audio
     - Transcript content analysis
     - Viral-worthiness scoring
   - Automated clip extraction and export
   - Optional caption overlays

5. **utils.py** - Helper functions
   - Google Drive link parsing
   - File validation
   - Time formatting
   - Processing time estimation

## 🔬 Technical Approach

### Phase 1: Audio Analysis
```
Video → Extract Audio → Analyze Features
                       ↓
                  RMS Energy
                  Zero Crossing Rate
                  Spectral Centroid
                       ↓
                  Peak Detection
```

### Phase 2: Content Understanding
```
Audio → Whisper Transcription → Timestamped Text
                                      ↓
                              Segment Analysis
                              Keyword Detection
```

### Phase 3: AI Selection
```
Transcript + Peaks → Google Gemini API → Viral Moment Analysis
                                              ↓
                                    5 Best Moments Identified
                                    (with timestamps, titles, hooks)
```

### Phase 4: Clip Generation
```
Selected Moments → Video Processing → Clip Extraction
                                           ↓
                                    Optional: Crop to 9:16
                                    Optional: Add Captions
                                           ↓
                                    Export MP4 Clips
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Streamlit | Web interface |
| Video Processing | MoviePy, OpenCV | Cutting, cropping, exporting |
| Audio Analysis | Librosa, SciPy | Feature extraction, peak detection |
| Transcription | OpenAI Whisper | Speech-to-text with timestamps |
| AI Analysis | Google Gemini 1.5 Flash | Content understanding, moment selection |
| Face Detection | MediaPipe | Smart cropping (optional) |
| Data Processing | NumPy | Numerical computations |

## 📊 Key Features

### Core Features (Mandatory)
✅ Emotional peak detection using audio analysis
✅ AI-powered moment identification with Google Gemini
✅ Automated clip generation (3-5 clips per video)
✅ Web-based interface with file upload
✅ Preview and download functionality

### Optional Features
🎯 Smart crop to vertical (9:16) format
🎯 Dynamic caption overlays
🎯 Face-tracking for centered framing
🎯 Configurable sensitivity and parameters

## 🎮 User Flow

1. **Upload**: User uploads long-form video (or provides Google Drive link)
2. **Configure**: Set number of clips, duration, and optional features
3. **Process**: Click "Generate Clips" button
   - Progress bar shows real-time status
   - Estimated time displayed
4. **Preview**: Generated clips shown with metadata
   - Title, time range, emotion score
   - Inline video preview
5. **Download**: Individual clip downloads as MP4 files

## 📈 Performance Metrics

- **Processing Speed**: ~2-5 minutes for a 30-minute video
- **Accuracy**: High-quality moment detection based on audio features
- **Clip Quality**: Full HD output with original audio quality
- **User Experience**: Simple, intuitive interface

## 🧪 Testing

Sample input video: [Input video for ByteSize Hackathon.mp4]

Expected outputs:
- 3-5 MP4 clips (15-90 seconds each)
- High-energy moments with strong engagement potential
- Proper audio/video sync
- Download-ready files

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Docker Deployment
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

### Cloud Deployment
- Streamlit Cloud
- Heroku
- Google Cloud Run
- AWS EC2

## 💪 Challenges Overcome

1. **Large Context Windows**: Used Gemini 1.5 Flash for 1M+ token context
2. **Accurate Timing**: Combined audio analysis with transcript timestamps
3. **Memory Efficiency**: Processed videos in chunks, cleaned up temp files
4. **User Experience**: Real-time progress feedback, error handling

## 🔮 Future Enhancements

- [ ] Google Drive integration for direct downloads
- [ ] Batch processing multiple videos
- [ ] Custom branding/watermarks
- [ ] Advanced caption styling with templates
- [ ] Multi-language support
- [ ] Speaker identification in multi-speaker videos
- [ ] Auto-posting to social media platforms
- [ ] Analytics dashboard for clip performance

## 📝 Code Quality

- Modular architecture with separate concerns
- Comprehensive error handling
- Type hints and documentation
- Clean, readable code
- Configuration options for flexibility

## 🎓 Learning Outcomes

- Multimodal AI integration (video, audio, text)
- Large language model prompting for content analysis
- Audio signal processing techniques
- Video manipulation with Python
- Full-stack application development

## 🏆 Hackathon Submission

**Repository**: [GitHub Link]
**Demo Video**: [YouTube/Drive Link]
**Live Demo**: [Streamlit Cloud Link]

### Submission Checklist
✅ Source code on GitHub
✅ README with setup instructions
✅ Screen recording of working project
✅ Sample input/output videos
✅ Documentation and comments

---

**Built with ❤️ for ByteSize Hackathon**
