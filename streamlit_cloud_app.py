"""
Simplified Streamlit application for Streamlit Cloud deployment.
This version has minimal dependencies and better error handling for cloud deployment.
"""

import streamlit as st
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import core components with error handling
CORE_IMPORTS_AVAILABLE = False
IMAGE_EMBEDDER_AVAILABLE = False
AUDIO_EMBEDDER_AVAILABLE = False

try:
    from ingestion.ingestor import Ingestor
    from retrieval.retriever import Retriever
    from generation.generator import Generator
    from indexing.vector_store import VectorStore
    from embedding.text_embedder import TextEmbedder
    from utils.config import config
    CORE_IMPORTS_AVAILABLE = True
    logger.info("Core imports successful")
except ImportError as e:
    logger.error(f"Core imports failed: {e}")
    st.error(f"Core system components not available: {e}")

# Try to import optional components
try:
    from embedding.image_embedder import ImageEmbedder
    IMAGE_EMBEDDER_AVAILABLE = True
    logger.info("Image embedder available")
except ImportError:
    ImageEmbedder = None
    logger.info("Image embedder not available")

try:
    from embedding.audio_embedder import AudioEmbedder
    AUDIO_EMBEDDER_AVAILABLE = True
    logger.info("Audio embedder available")
except ImportError:
    AudioEmbedder = None
    logger.info("Audio embedder not available")

def check_system_status():
    """Check system status and show available features."""
    st.sidebar.header("System Status")
    
    if CORE_IMPORTS_AVAILABLE:
        st.sidebar.success("✅ Core system ready")
    else:
        st.sidebar.error("❌ Core system not available")
    
    if IMAGE_EMBEDDER_AVAILABLE:
        st.sidebar.success("✅ Image processing available")
    else:
        st.sidebar.info("ℹ️ Image processing not available")
    
    if AUDIO_EMBEDDER_AVAILABLE:
        st.sidebar.success("✅ Audio processing available")
    else:
        st.sidebar.info("ℹ️ Audio processing not available")

def show_welcome():
    """Show welcome message and instructions."""
    st.title("🔍 Multimodal RAG System")
    
    st.markdown("""
    ### Welcome to the Multimodal RAG System!
    
    This system can process documents, images, and audio files to provide intelligent search 
    and question answering capabilities.
    
    _Optimized for Streamlit Cloud deployment_
    """)
    
    # Show available features
    st.subheader("Available Features")
    
    if CORE_IMPORTS_AVAILABLE:
        st.success("✅ Text Processing: Process TXT, DOCX, and PDF documents")
        st.success("✅ Question Answering: Ask questions about your content")
        st.success("✅ Semantic Search: Find relevant content using natural language")
    else:
        st.error("❌ Core features not available due to missing dependencies")
    
    if IMAGE_EMBEDDER_AVAILABLE:
        st.success("✅ Image Processing: Process PNG, JPG, and JPEG images")
    else:
        st.info("ℹ️ Image Processing: Not available in this deployment")
    
    if AUDIO_EMBEDDER_AVAILABLE:
        st.success("✅ Audio Processing: Process MP3 and WAV audio files")
    else:
        st.info("ℹ️ Audio Processing: Not available in this deployment")

def show_troubleshooting():
    """Show troubleshooting information."""
    st.subheader("Troubleshooting")
    
    st.markdown("""
    ### Common Issues on Streamlit Cloud
    
    1. **Dependency Issues**: 
       - Some packages may not install correctly on Streamlit Cloud
       - The system gracefully degrades when packages are missing
    
    2. **Memory Limitations**:
       - Streamlit Cloud has memory constraints
       - Large models or files may cause issues
    
    3. **Build Timeouts**:
       - Initial deployment may take several minutes due to model downloads
       - Subsequent runs are faster due to caching
    
    ### If You're Still Experiencing Issues
    
    1. Check the build logs in Streamlit Cloud for specific error messages
    2. Try using the simplified requirements file: `requirements_streamlit_cloud.txt`
    3. Verify that your forked repository is up to date
    4. Check that `streamlit_app.py` is in the root directory
    """)

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Multimodal RAG System - Streamlit Cloud",
        page_icon="🔍",
        layout="wide"
    )
    
    # Check system status
    check_system_status()
    
    # Show welcome and instructions
    show_welcome()
    
    # Show troubleshooting information
    show_troubleshooting()
    
    # Show next steps
    st.subheader("Next Steps")
    
    if CORE_IMPORTS_AVAILABLE:
        st.markdown("""
        1. The system is ready to use!
        2. Go to the **Ingest** tab to upload and process your files
        3. Use the **Chat** tab to ask questions about your content
        4. Check the **Status** tab to see system information
        """)
    else:
        st.markdown("""
        1. Check your requirements file and Streamlit Cloud setup
        2. Refer to the deployment documentation for troubleshooting
        3. Make sure all required packages are specified in your requirements
        """)

if __name__ == "__main__":
    main()