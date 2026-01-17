@echo off
echo ========================================
echo   PulsePoint AI - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [1/4] Creating virtual environment...
    python -m venv .venv
    echo     Virtual environment created!
) else (
    echo [1/4] Virtual environment found!
)

echo.
echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [3/4] Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo [4/4] Starting PulsePoint AI...
echo.
echo ========================================
echo   App will open in your browser
echo   Default: http://localhost:8501
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
