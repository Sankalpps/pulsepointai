"""
Quick test script to verify installation and basic functionality
"""
import sys

def check_installation():
    """Check if all required packages are installed"""
    
    print("🔍 Checking PulsePoint AI Installation...\n")
    
    required_packages = {
        'streamlit': 'Streamlit',
        'moviepy': 'MoviePy',
        'whisper': 'OpenAI Whisper',
        'google.generativeai': 'Google Generative AI',
        'mediapipe': 'MediaPipe',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'librosa': 'Librosa',
        'scipy': 'SciPy'
    }
    
    missing_packages = []
    installed_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            installed_packages.append(name)
            print(f"✅ {name}")
        except ImportError:
            missing_packages.append(name)
            print(f"❌ {name} - NOT INSTALLED")
    
    print(f"\n📊 Summary:")
    print(f"   Installed: {len(installed_packages)}/{len(required_packages)}")
    print(f"   Missing: {len(missing_packages)}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print(f"\n💡 To install missing packages, run:")
        print(f"   pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All packages installed successfully!")
        return True


def check_ffmpeg():
    """Check if FFmpeg is available"""
    import subprocess
    
    print("\n🎬 Checking FFmpeg...")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg found: {version_line}")
            return True
        else:
            print("❌ FFmpeg not found")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg not found in PATH")
        print("\n💡 Install FFmpeg:")
        print("   Windows: choco install ffmpeg")
        print("   Mac: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Error checking FFmpeg: {str(e)}")
        return False


def test_basic_functionality():
    """Test basic video processing functionality"""
    
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        # Test MoviePy
        from moviepy import ColorClip
        clip = ColorClip(size=(100, 100), color=(255, 0, 0), duration=1)
        clip.close()
        print("✅ MoviePy working")
        
        # Test Whisper model loading (without downloading)
        import whisper
        print("✅ Whisper module loaded")
        
        # Test Gemini import
        import google.generativeai as genai
        print("✅ Google Generative AI module loaded")
        
        # Test MediaPipe
        import mediapipe as mp
        print("✅ MediaPipe loaded")
        
        # Test Librosa
        import librosa
        print("✅ Librosa loaded")
        
        print("\n✅ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        return False


def main():
    """Main test function"""
    
    print("=" * 60)
    print("  PulsePoint AI - Installation Verification")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"\n🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("⚠️  Warning: Python 3.8 or higher is recommended")
    
    # Run checks
    packages_ok = check_installation()
    ffmpeg_ok = check_ffmpeg()
    
    if packages_ok:
        functionality_ok = test_basic_functionality()
    else:
        functionality_ok = False
    
    # Final summary
    print("\n" + "=" * 60)
    if packages_ok and ffmpeg_ok and functionality_ok:
        print("🎉 Installation verified! You're ready to use PulsePoint AI")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some issues found. Please fix them before running the app.")
    print("=" * 60)


if __name__ == "__main__":
    main()
