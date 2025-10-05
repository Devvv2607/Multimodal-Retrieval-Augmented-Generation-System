@echo off
echo Setting up Multimodal RAG Environment...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Installing CLIP from OpenAI repository...
pip install git+https://github.com/openai/CLIP.git
if %errorlevel% neq 0 (
    echo Failed to install CLIP.
    pause
    exit /b 1
)

echo Initializing system directories...
python init.py
if %errorlevel% neq 0 (
    echo Failed to initialize system directories.
    pause
    exit /b 1
)

echo Setup complete! 
echo To activate the environment in the future, run: venv\Scripts\activate.bat
echo To download models, run: python models\setup_models.py
echo To run the system, use: python main.py --help
pause