#!/bin/bash

# Deployment script for Multimodal RAG System
# This script automates the deployment process on Unix-like systems

set -e  # Exit on any error

echo ".Multimodal RAG System Deployment Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" < "3.8" ]]
then
    echo "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "Python version $PYTHON_VERSION is compatible."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv rag_env

# Activate virtual environment
echo "Activating virtual environment..."
source rag_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Install additional packages
echo "Installing additional packages..."
pip install git+https://github.com/openai/CLIP.git
pip install streamlit

# Initialize the system
echo "Initializing the system..."
python init.py

echo "Deployment completed successfully!"

echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source rag_env/bin/activate"
echo "2. Run the Streamlit app: streamlit run streamlit_app.py"
echo ""
echo "The app will be available at http://localhost:8501"