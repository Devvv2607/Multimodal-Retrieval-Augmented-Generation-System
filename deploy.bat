@echo off
REM Deployment script for Multimodal RAG System
REM This script automates the deployment process on Windows systems

echo.Multimodal RAG System Deployment Script
echo.========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo.Python version: %PYTHON_VERSION%

REM Create virtual environment
echo.Creating virtual environment...
python -m venv rag_env

REM Activate virtual environment
echo.Activating virtual environment...
call rag_env\Scripts\activate

REM Upgrade pip
echo.Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.Installing requirements...
pip install -r requirements.txt

REM Install additional packages
echo.Installing additional packages...
pip install git+https://github.com/openai/CLIP.git
pip install streamlit

REM Initialize the system
echo.Initializing the system...
python init.py

echo.Deployment completed successfully!

echo.
echo.To run the application:
echo.1. Activate the virtual environment: rag_env\Scripts\activate
echo.2. Run the Streamlit app: streamlit run streamlit_app.py
echo.
echo.The app will be available at http://localhost:8501

pause