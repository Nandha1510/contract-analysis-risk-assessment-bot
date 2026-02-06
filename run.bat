@echo off
REM Contract Analysis & Risk Assessment Bot - Batch Setup & Run Script
REM For Windows Command Prompt Users

echo.
echo ============================================================
echo   Contract Analysis ^& Risk Assessment Bot
echo   Setup and Launch Script
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [1/5] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
)

REM Download spaCy model
echo [4/5] Downloading spaCy model...
python -m spacy download en_core_web_sm >nul 2>&1

REM Launch Streamlit app
echo [5/5] Launching Streamlit app...
echo.
echo ============================================================
echo   App is starting at http://localhost:8501
echo   Press Ctrl+C to stop the app
echo ============================================================
echo.

streamlit run app.py

REM Keep window open on error
pause
