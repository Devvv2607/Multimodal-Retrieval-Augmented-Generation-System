"""
Setup script for deployment environments.
This script helps set up the environment for deployment on various platforms.
"""

import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements(requirements_file="requirements.txt"):
    """Install requirements from a file."""
    try:
        logger.info(f"Installing requirements from {requirements_file}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        logger.info("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False

def install_clip():
    """Install CLIP from GitHub."""
    try:
        logger.info("Installing CLIP from GitHub")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "git+https://github.com/openai/CLIP.git"])
        logger.info("CLIP installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install CLIP: {e}")
        return False

def install_whisper():
    """Install Whisper."""
    try:
        logger.info("Installing Whisper")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
        logger.info("Whisper installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Whisper: {e}")
        return False

def install_streamlit():
    """Install Streamlit."""
    try:
        logger.info("Installing Streamlit")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        logger.info("Streamlit installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Streamlit: {e}")
        return False

def check_imports():
    """Check if all required imports are available."""
    required_imports = [
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss-cpu"),
        ("numpy", "numpy"),
        ("PIL", "pillow"),
        ("docx", "python-docx"),
        ("PyPDF2", "pypdf2")
    ]
    
    missing_imports = []
    
    for import_name, package_name in required_imports:
        try:
            __import__(import_name)
            logger.info(f"✓ {import_name} imported successfully")
        except ImportError:
            logger.error(f"✗ {import_name} not available (package: {package_name})")
            missing_imports.append((import_name, package_name))
    
    # Check optional imports
    try:
        import clip
        logger.info("✓ CLIP imported successfully")
    except ImportError:
        logger.warning("⚠ CLIP not available (optional)")
    
    try:
        import whisper
        logger.info("✓ Whisper imported successfully")
    except ImportError:
        logger.warning("⚠ Whisper not available (optional)")
    
    try:
        import streamlit
        logger.info("✓ Streamlit imported successfully")
    except ImportError:
        logger.warning("⚠ Streamlit not available (optional)")
    
    return len(missing_imports) == 0, missing_imports

def setup_deployment_environment():
    """Set up the deployment environment."""
    logger.info("Setting up deployment environment...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install core requirements
    if not install_requirements("requirements.txt"):
        logger.error("Failed to install core requirements")
        return False
    
    # Install optional packages
    install_clip()
    install_whisper()
    install_streamlit()
    
    # Check imports
    all_good, missing = check_imports()
    
    if all_good:
        logger.info("✅ Deployment environment setup completed successfully!")
        logger.info("You can now run the Streamlit app with: streamlit run streamlit_app.py")
        return True
    else:
        logger.warning("⚠ Deployment environment setup completed with some issues")
        logger.info("Missing packages:")
        for import_name, package_name in missing:
            logger.info(f"  - {package_name} (for {import_name})")
        logger.info("The application will run with limited functionality.")
        return True

def setup_streamlit_cloud():
    """Set up environment for Streamlit Cloud."""
    logger.info("Setting up Streamlit Cloud environment...")
    
    # For Streamlit Cloud, we use the simplified requirements
    if not install_requirements("requirements_streamlit.txt"):
        logger.error("Failed to install Streamlit Cloud requirements")
        return False
    
    # Try to install optional packages
    install_clip()
    install_whisper()
    
    # Check imports
    all_good, missing = check_imports()
    
    if all_good:
        logger.info("✅ Streamlit Cloud environment setup completed successfully!")
        return True
    else:
        logger.warning("⚠ Streamlit Cloud environment setup completed with some issues")
        logger.info("Missing packages:")
        for import_name, package_name in missing:
            logger.info(f"  - {package_name} (for {import_name})")
        logger.info("The application will run with limited functionality.")
        return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup deployment environment")
    parser.add_argument("--streamlit-cloud", action="store_true", 
                        help="Setup for Streamlit Cloud deployment")
    parser.add_argument("--verbose", action="store_true", 
                        help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.streamlit_cloud:
        success = setup_streamlit_cloud()
    else:
        success = setup_deployment_environment()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)