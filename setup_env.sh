#!/bin/bash

echo "Setting up Multimodal RAG Environment..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python found. Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

echo "Installing CLIP from OpenAI repository..."
pip install git+https://github.com/openai/CLIP.git
if [ $? -ne 0 ]; then
    echo "Failed to install CLIP."
    exit 1
fi

echo "Initializing system directories..."
python init.py
if [ $? -ne 0 ]; then
    echo "Failed to initialize system directories."
    exit 1
fi

echo "Setup complete!"
echo "To activate the environment in the future, run: source venv/bin/activate"
echo "To download models, run: python models/setup_models.py"
echo "To run the system, use: python main.py --help"