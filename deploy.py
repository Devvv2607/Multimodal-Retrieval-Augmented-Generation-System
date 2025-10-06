"""
Deployment script for Streamlit Cloud.
This script handles dependency checking and graceful degradation.
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
try:
    from ingestion.ingestor import Ingestor
    from retrieval.retriever import Retriever
    from generation.generator import Generator
    from indexing.vector_store import VectorStore
    from embedding.text_embedder import TextEmbedder
    from utils.config import config
    CORE_IMPORTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Core imports failed: {e}")
    CORE_IMPORTS_AVAILABLE = False

# Import optional components with graceful fallback
try:
    from embedding.image_embedder import ImageEmbedder
    IMAGE_EMBEDDER_AVAILABLE = True
except ImportError:
    ImageEmbedder = None
    IMAGE_EMBEDDER_AVAILABLE = False
    st.warning("Image processing not available (CLIP not installed)")

try:
    from embedding.audio_embedder import AudioEmbedder
    AUDIO_EMBEDDER_AVAILABLE = True
except ImportError:
    AudioEmbedder = None
    AUDIO_EMBEDDER_AVAILABLE = False
    st.warning("Audio processing not available (Whisper not installed)")

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

def show_deployment_info():
    """Show deployment-specific information."""
    st.header("Streamlit Cloud Deployment")
    st.markdown("""
    This application is configured for deployment on Streamlit Cloud.
    
    ## Deployment Information
    
    ### Resource Management
    - The system is configured to use CPU-only mode to avoid GPU-related issues
    - Models are cached after first download
    - Memory usage is optimized for Streamlit Cloud limitations
    
    ### Feature Availability
    The application will automatically adapt to the available packages:
    """)
    
    features = []
    features.append("📄 **Text Processing**: Process TXT, DOCX, and PDF documents")
    features.append("💬 **Question Answering**: Ask questions about your indexed content")
    features.append("🔍 **Semantic Search**: Find relevant content using natural language")
    
    if IMAGE_EMBEDDER_AVAILABLE:
        features.append("🖼️ **Image Processing**: Process PNG, JPG, and JPEG images")
    else:
        features.append("ℹ️ **Image Processing**: Not available in this deployment")
    
    if AUDIO_EMBEDDER_AVAILABLE:
        features.append("🔊 **Audio Processing**: Process MP3 and WAV audio files")
    else:
        features.append("ℹ️ **Audio Processing**: Not available in this deployment")
    
    for feature in features:
        st.markdown(feature)
    
    st.markdown("""
    ### File Size Limitations
    - Streamlit Cloud has file size limits for uploads
    - For best performance, use smaller files (< 10MB each)
    
    ### Model Download
    - Models will be downloaded on first use
    - This may take a few minutes
    - Subsequent runs will be faster due to caching
    
    ### Troubleshooting
    If you encounter issues:
    1. Check the Streamlit Cloud build logs
    2. Verify all requirements are correctly specified
    3. Ensure your repository structure matches the expected format
    """)

def main():
    """Main deployment application."""
    st.set_page_config(
        page_title="Multimodal RAG System - Streamlit Cloud",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Multimodal Retrieval-Augmented Generation System")
    
    # Check system status
    check_system_status()
    
    # Show deployment information
    show_deployment_info()
    
    if not CORE_IMPORTS_AVAILABLE:
        st.error("The system cannot start due to missing core dependencies.")
        st.info("Please check your requirements file and Streamlit Cloud setup.")
        st.info("Refer to STREAMLIT_CLOUD_DEPLOYMENT.md for detailed instructions.")
        return
    
    st.markdown("""
    ## Getting Started:
    1. Go to the **Ingest** tab to upload and process your files
    2. Use the **Chat** tab to ask questions about your content
    3. Check the **Status** tab to see system information
    
    ### For Streamlit Cloud Users:
    - This application is optimized for Streamlit Cloud deployment
    - Features will automatically adapt to available packages
    - Refer to the documentation for detailed deployment instructions
    """)

if __name__ == "__main__":
    main()