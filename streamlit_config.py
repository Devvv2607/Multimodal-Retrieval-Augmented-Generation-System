"""
Streamlit configuration and dependency management.
"""

import logging
import sys

logger = logging.getLogger(__name__)

# List of required packages
REQUIRED_PACKAGES = [
    "transformers",
    "torch",
    "sentence-transformers",
    "faiss-cpu",
    "numpy",
    "pillow",
    "python-docx",
    "pypdf2",
    "openai-whisper",
    "ftfy",
    "regex",
    "tqdm",
    "pyyaml"
]

def check_dependencies():
    """
    Check if all required dependencies are available.
    
    Returns:
        tuple: (bool, list) - (all_available, missing_packages)
    """
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            if package == "openai-whisper":
                import whisper
            elif package == "sentence-transformers":
                import sentence_transformers
            elif package == "python-docx":
                import docx
            elif package == "pypdf2":
                import PyPDF2
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"Package not found: {package}")
    
    # Check for CLIP separately as it's installed via git
    try:
        import clip
    except ImportError:
        missing_packages.append("clip (git+https://github.com/openai/CLIP.git)")
        logger.warning("CLIP not found")
    
    all_available = len(missing_packages) == 0
    
    if not all_available:
        logger.warning(f"Missing packages: {missing_packages}")
    
    return all_available, missing_packages

def install_instructions():
    """
    Provide installation instructions for missing packages.
    
    Returns:
        str: Installation instructions
    """
    instructions = """
# Installation Instructions

To install all required dependencies, run:

```bash
pip install -r requirements.txt
```

For CLIP (installed via git):
```bash
pip install git+https://github.com/openai/CLIP.git
```

For Whisper (if not installed via requirements.txt):
```bash
pip install openai-whisper
```

Note: Some packages may require additional system dependencies.
On Ubuntu/Debian, you might need:
```bash
sudo apt-get install ffmpeg
```

On Windows, you might need to install Visual Studio Build Tools.
"""
    return instructions

if __name__ == "__main__":
    # Run dependency check
    all_available, missing = check_dependencies()
    
    if all_available:
        print("All dependencies are available!")
        sys.exit(0)
    else:
        print(f"Missing dependencies: {missing}")
        print(install_instructions())
        sys.exit(1)