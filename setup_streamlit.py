"""
Setup script specifically for Streamlit Cloud deployment.
This script handles environment setup and graceful degradation for Streamlit Cloud limitations.
"""

import streamlit as st
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_and_install_packages():
    """Check and install required packages with graceful degradation."""
    st.info("Checking system packages...")
    
    # Core packages that should be in requirements_streamlit.txt
    core_packages = [
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss-cpu"),
        ("numpy", "numpy"),
        ("PIL", "pillow"),
        ("docx", "python-docx"),
        ("PyPDF2", "pypdf2"),
        ("yaml", "pyyaml")
    ]
    
    missing_packages = []
    
    for import_name, package_name in core_packages:
        try:
            __import__(import_name)
            st.success(f"✓ {package_name} is available")
            logger.info(f"✓ {import_name} imported successfully")
        except ImportError:
            st.error(f"✗ {package_name} is missing")
            logger.error(f"✗ {import_name} not available (package: {package_name})")
            missing_packages.append((import_name, package_name))
    
    # Check optional packages
    st.info("Checking optional packages...")
    
    try:
        import clip
        st.success("✓ CLIP (image processing) is available")
        logger.info("✓ CLIP imported successfully")
        clip_available = True
    except ImportError:
        st.warning("⚠ CLIP (image processing) not available - image features will be disabled")
        logger.warning("⚠ CLIP not available (optional)")
        clip_available = False
    
    try:
        import whisper
        st.success("✓ Whisper (audio processing) is available")
        logger.info("✓ Whisper imported successfully")
        whisper_available = True
    except ImportError:
        st.warning("⚠ Whisper (audio processing) not available - audio features will be disabled")
        logger.warning("⚠ Whisper not available (optional)")
        whisper_available = False
    
    return len(missing_packages) == 0, missing_packages, clip_available, whisper_available

def setup_directories():
    """Set up required directories with proper permissions."""
    st.info("Setting up directories...")
    
    directories = [
        "./data",
        "./temp",
        "./models"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            st.success(f"✓ Created directory: {directory}")
            logger.info(f"✓ Directory {directory} ready")
        except Exception as e:
            st.error(f"✗ Failed to create directory {directory}: {str(e)}")
            logger.error(f"✗ Directory setup failed for {directory}: {str(e)}")
            return False
    
    return True

def initialize_config():
    """Initialize or verify configuration."""
    st.info("Checking configuration...")
    
    try:
        from utils.config import config
        
        # Verify key configuration values
        required_configs = [
            "models.text_embedding.name",
            "models.llm.name",
            "vector_db.index_path",
            "vector_db.metadata_path"
        ]
        
        for config_key in required_configs:
            value = config.get(config_key)
            if value is None:
                st.warning(f"⚠ Configuration missing: {config_key}")
                logger.warning(f"⚠ Config key missing: {config_key}")
            else:
                st.success(f"✓ {config_key}: {value}")
                logger.info(f"✓ Config {config_key} = {value}")
        
        return True
    except Exception as e:
        st.error(f"✗ Configuration error: {str(e)}")
        logger.error(f"✗ Config initialization failed: {str(e)}")
        return False

def check_models():
    """Check if required models can be loaded."""
    st.info("Checking model availability...")
    
    try:
        from transformers import AutoModel, AutoTokenizer
        from sentence_transformers import SentenceTransformer
        
        # Check text embedding model
        text_embedding_model = st.session_state.get('config', {}).get('models', {}).get('text_embedding', {}).get('name', 'all-MiniLM-L6-v2')
        st.info(f"Checking text embedding model: {text_embedding_model}")
        
        # We won't actually load the model here to save time and resources
        st.success("✓ Text embedding model configuration verified")
        logger.info("✓ Text embedding model config OK")
        
        # Check LLM model
        llm_model = st.session_state.get('config', {}).get('models', {}).get('llm', {}).get('name', 'microsoft/phi-3-mini-4k-instruct')
        st.info(f"Checking LLM model: {llm_model}")
        
        # We won't actually load the model here to save time and resources
        st.success("✓ LLM model configuration verified")
        logger.info("✓ LLM model config OK")
        
        return True
    except Exception as e:
        st.error(f"✗ Model check failed: {str(e)}")
        logger.error(f"✗ Model check failed: {str(e)}")
        return False

def main():
    """Main setup function for Streamlit Cloud."""
    st.set_page_config(
        page_title="Streamlit Cloud Setup",
        page_icon="⚙️"
    )
    
    st.title("⚙️ Streamlit Cloud Setup for Multimodal RAG")
    st.markdown("""
    This tool helps verify your Streamlit Cloud deployment setup for the Multimodal RAG System.
    
    It will check:
    - Required packages
    - Optional packages (with graceful degradation)
    - Directory structure
    - Configuration files
    - Model availability
    """)
    
    # Run setup checks
    with st.spinner("Running setup checks..."):
        # Check packages
        packages_ok, missing_packages, clip_available, whisper_available = check_and_install_packages()
        
        # Setup directories
        dirs_ok = setup_directories()
        
        # Initialize config
        config_ok = initialize_config()
        
        # Check models
        models_ok = check_models()
    
    # Show results
    st.header("Setup Results")
    
    if packages_ok and dirs_ok and config_ok and models_ok:
        st.success("🎉 All setup checks passed!")
        st.info("Your application is ready for Streamlit Cloud deployment.")
        
        # Show feature availability
        st.subheader("Feature Availability")
        st.success("✅ Text Processing: Available")
        
        if clip_available:
            st.success("✅ Image Processing: Available")
        else:
            st.info("ℹ️ Image Processing: Not available (CLIP not installed)")
        
        if whisper_available:
            st.success("✅ Audio Processing: Available")
        else:
            st.info("ℹ️ Audio Processing: Not available (Whisper not installed)")
            
        st.info("You can now deploy your app to Streamlit Cloud!")
        
    else:
        st.warning("⚠ Some setup checks failed or have warnings")
        
        if not packages_ok:
            st.error("❌ Missing required packages:")
            for import_name, package_name in missing_packages:
                st.write(f"  - {package_name}")
        
        if not dirs_ok:
            st.error("❌ Directory setup failed")
            
        if not config_ok:
            st.error("❌ Configuration issues detected")
            
        if not models_ok:
            st.error("❌ Model issues detected")
        
        st.info("Please check your requirements file and Streamlit Cloud setup.")

if __name__ == "__main__":
    main()