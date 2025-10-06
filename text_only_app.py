"""
Text-only Streamlit application for the RAG System.
This is a simplified version that only handles text documents.
"""

import streamlit as st
import os
import sys
import tempfile
from typing import List, Dict, Any
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our RAG system components with error handling
try:
    from ingestion.ingestor import Ingestor
    from retrieval.retriever import Retriever
    from generation.generator import Generator
    from indexing.vector_store import VectorStore
    from embedding.text_embedder import TextEmbedder
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Import error: {str(e)}")
    IMPORTS_AVAILABLE = False

from utils.config import config

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'diagnostics' not in st.session_state:
    st.session_state.diagnostics = []

def log_diagnostic(message):
    """Log diagnostic information."""
    st.session_state.diagnostics.append(message)
    logger.info(message)

def initialize_system():
    """Initialize the RAG system components for text-only processing."""
    if not IMPORTS_AVAILABLE:
        st.error("Required dependencies are not available. Please check the installation.")
        return False
        
    try:
        log_diagnostic("Initializing text-only system components...")
        
        # Initialize components
        st.session_state.vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        log_diagnostic("Vector store initialized")
        
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        log_diagnostic("Text embedder initialized")
        
        # Initialize retriever with only text embedder (no image embedder)
        st.session_state.retriever = Retriever(
            st.session_state.vector_store, 
            text_embedder, 
            None  # No image embedder for text-only version
        )
        log_diagnostic("Retriever initialized (text-only)")
        
        st.session_state.generator = Generator(
            model_name=config.get('models.llm.name'),
            max_tokens=config.get('models.llm.max_tokens', 2048),
            force_cpu=True  # Force CPU to avoid device-related errors
        )
        
        # Log device status
        if hasattr(st.session_state.generator, 'device'):
            log_diagnostic(f"Model loaded on device: {st.session_state.generator.device}")
        
        log_diagnostic("Generator initialized")
        
        if st.session_state.generator.model is not None:
            log_diagnostic("LLM model loaded successfully")
        else:
            log_diagnostic("LLM model not loaded - using fallback mode")
        
        st.session_state.initialized = True
        log_diagnostic("Text-only system initialization complete")
        return True
    except Exception as e:
        error_msg = f"Error initializing system: {str(e)}"
        log_diagnostic(error_msg)
        st.error(error_msg)
        return False

def main():
    """Main Streamlit application for text-only version."""
    st.set_page_config(
        page_title="Text-only RAG System",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Text-only Retrieval-Augmented Generation System")
    st.markdown("""
    This system processes text documents to provide intelligent search and question answering capabilities.
    Upload your text files and ask questions!
    """)
    
    # Show warning if imports are not available
    if not IMPORTS_AVAILABLE:
        st.warning("Some dependencies are not available. The system may have limited functionality.")
        st.info("Please check that all required packages are installed correctly.")
        return
    
    # Initialize system if not already done
    if 'initialized' not in st.session_state or not st.session_state.initialized:
        with st.spinner("Initializing system..."):
            if not initialize_system():
                st.error("Failed to initialize the system. Please check the logs.")
                return
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Text Ingest", "💬 Chat", "📊 Status", "ℹ️ About"])
    
    with tab1:
        st.header("Text Document Ingestion")
        st.markdown("Upload text documents to be processed and indexed by the system.")
        
        uploaded_files = st.file_uploader(
            "Choose text files to ingest",
            accept_multiple_files=True,
            type=["txt", "docx", "pdf"]
        )
        
        if uploaded_files:
            st.info(f"Selected {len(uploaded_files)} files for ingestion.")
            
            if st.button("Process Text Files"):
                with st.spinner("Processing files..."):
                    try:
                        log_diagnostic(f"Processing {len(uploaded_files)} text files")
                        
                        # Create temporary directory for uploaded files
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Save uploaded files to temporary directory
                            file_paths = []
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                file_paths.append(file_path)
                                log_diagnostic(f"Saved file: {file_path}")
                            
                            # Initialize ingestor with the session state vector store
                            ingestor = Ingestor()
                            # Replace the ingestor's vector store with the session state one
                            ingestor.vector_store = st.session_state.vector_store
                            log_diagnostic("Ingestor initialized with session vector store")
                            
                            # Process each file
                            processed_count = 0
                            for file_path in file_paths:
                                log_diagnostic(f"Processing file: {file_path}")
                                if ingestor._process_file(file_path):
                                    processed_count += 1
                                    log_diagnostic(f"Successfully processed: {file_path}")
                                else:
                                    log_diagnostic(f"Failed to process: {file_path}")
                            
                            st.success(f"Successfully processed {processed_count} out of {len(uploaded_files)} files!")
                            log_diagnostic(f"Processing complete: {processed_count}/{len(uploaded_files)} files processed")
                            
                            # Show system status
                            total_vectors = st.session_state.vector_store.get_total_vectors()
                            st.info(f"Total indexed vectors: {total_vectors}")
                            log_diagnostic(f"Total vectors after processing: {total_vectors}")
                            
                    except Exception as e:
                        error_msg = f"Error processing files: {str(e)}"
                        st.error(error_msg)
                        log_diagnostic(error_msg)
        
        st.markdown("### Supported Text File Types")
        st.markdown("""
        - **Plain Text**: .txt
        - **Word Documents**: .docx
        - **PDF Documents**: .pdf
        """)
    
    with tab2:
        st.header("Chat Interface")
        st.markdown("Ask questions about your indexed text content.")
        
        # Add custom CSS to fix the chat input at the bottom
        st.markdown("""
        <style>
        /* Target all possible chat input containers */
        .stChatFloatingInputContainer,
        [data-testid="stChatInput"],
        [data-testid="stChatInputContainer"] {
            position: fixed !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            background-color: white !important;
            padding: 1rem !important;
            border-top: 1px solid #e0e0e0 !important;
            z-index: 999999 !important;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
        }
        
        /* Add padding to bottom of main container */
        .main .block-container {
            padding-bottom: 150px !important;
        }
        
        /* Add padding to chat messages */
        [data-testid="stChatMessageContainer"],
        .stChatMessage {
            margin-bottom: 1rem !important;
        }
        
        /* Ensure proper spacing at bottom of chat */
        section[data-testid="stVerticalBlock"] > div:last-child {
            padding-bottom: 120px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display chat history
        if 'chat_history' in st.session_state:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message to chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            log_diagnostic(f"User query: {prompt}")
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Process the query
            with st.chat_message("assistant"):
                status_placeholder = st.empty()
                status_placeholder.markdown("🔍 Retrieving relevant information...")
                
                try:
                    log_diagnostic("Starting retrieval process")
                    
                    # Retrieve context (text-only)
                    context = st.session_state.retriever.retrieve_text(prompt, k=5)
                    log_diagnostic(f"Retrieved {len(context)} results")
                    
                    status_placeholder.markdown("🧠 Generating answer...")
                    
                    response_content = ""
                    if context:
                        # Filter context to only include text items
                        text_context = [item for item in context if item.get('type') == 'text']
                        log_diagnostic(f"Filtered to {len(text_context)} text items")
                        
                        # Generate answer
                        answer_displayed = False
                        if st.session_state.generator.model is not None and text_context:
                            log_diagnostic("Generating answer with LLM")
                            try:
                                answer = st.session_state.generator.generate_answer(prompt, text_context)
                                status_placeholder.empty()
                                st.markdown(answer)
                                answer_displayed = True
                                response_content = answer
                                log_diagnostic("Answer generated and displayed successfully")
                                log_diagnostic(f"Generated answer length: {len(answer)} characters")
                            except Exception as gen_error:
                                log_diagnostic(f"Error generating answer: {str(gen_error)}")
                                status_placeholder.empty()
                                st.error(f"Error generating answer: {str(gen_error)}")
                                response_content = f"Error generating answer: {str(gen_error)}"
                        else:
                            # Fallback when LLM is not available or no text context
                            status_placeholder.empty()
                            if text_context:
                                st.markdown("**Note:** The LLM model is not available. Here's the relevant context I found:")
                                response_content = "**Note:** The LLM model is not available. Here's the relevant context I found:\n\n"
                                for i, item in enumerate(text_context, 1):
                                    source = os.path.basename(item.get('source', 'Unknown'))
                                    text = item.get('text', '')[:200] + "..." if len(item.get('text', '')) > 200 else item.get('text', '')
                                    st.markdown(f"**{i}.** {text} \n\n*Source: {source}*")
                                    response_content += f"**{i}.** {text} \n\n*Source: {source}*\n\n"
                            else:
                                st.markdown("I couldn't find any relevant text information to answer your question.")
                                response_content = "I couldn't find any relevant text information to answer your question."
                            answer_displayed = True
                            log_diagnostic("Showing fallback context")
                        
                        # Always display sources if we have text context
                        if text_context:
                            with st.expander("📚 Sources", expanded=False):
                                for i, item in enumerate(text_context, 1):
                                    source = os.path.basename(item.get('source', 'Unknown'))
                                    text = item.get('text', '')[:100] + "..." if len(item.get('text', '')) > 100 else item.get('text', '')
                                    st.markdown(f"**{i}.** {text} \n\n*Source: {source}*")
                        
                        # If no answer was displayed for some reason, show a message
                        if not answer_displayed:
                            status_placeholder.empty()
                            st.markdown("I processed your query but couldn't generate a response. Please check the diagnostics tab for more information.")
                            response_content = "I processed your query but couldn't generate a response."
                    else:
                        status_placeholder.empty()
                        st.markdown("I couldn't find any relevant information to answer your question.")
                        log_diagnostic("No relevant context found")
                        response_content = "I couldn't find any relevant information to answer your question."
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response_content})
                    log_diagnostic("Response added to chat history")
                    
                except Exception as e:
                    status_placeholder.empty()
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    log_diagnostic(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
    
    with tab3:
        st.header("System Status")
        
        if 'initialized' in st.session_state and st.session_state.initialized:
            total_vectors = st.session_state.vector_store.get_total_vectors()
            st.metric("Indexed Vectors", total_vectors)
            
            # Show index path
            st.subheader("Configuration")
            st.text(f"Index Path: {config.get('vector_db.index_path')}")
            st.text(f"Metadata Path: {config.get('vector_db.metadata_path')}")
            
            # Show models
            st.subheader("Models")
            st.text(f"Text Embedding: {config.get('models.text_embedding.name')}")
            st.text(f"LLM: {config.get('models.llm.name')}")
            
            # Show LLM status
            if st.session_state.generator.model is not None:
                st.success("✅ LLM Model: Loaded successfully")
            else:
                st.warning("⚠️ LLM Model: Not available (using fallback mode)")
            
            # Show metadata if available
            if total_vectors > 0:
                st.subheader("Indexed Content")
                try:
                    # Load metadata
                    import json
                    with open(config.get('vector_db.metadata_path'), 'r') as f:
                        metadata = json.load(f)
                    
                    # Create a summary (text-only)
                    text_count = sum(1 for item in metadata if item.get('type') == 'text')
                    sources = set()
                    for item in metadata:
                        if item.get('type') == 'text':
                            sources.add(os.path.basename(item.get('source', 'Unknown')))
                    
                    # Display summary
                    st.markdown("#### Content Summary")
                    st.text(f"Text Documents: {text_count} items")
                    
                    st.markdown("#### Indexed Sources")
                    for source in list(sources)[:10]:  # Show first 10 sources
                        st.text(f"• {source}")
                    
                    if len(sources) > 10:
                        st.text(f"... and {len(sources) - 10} more")
                        
                except Exception as e:
                    st.warning(f"Could not load metadata: {str(e)}")
        else:
            st.warning("System not initialized")
    
    with tab4:
        st.header("About This System")
        st.markdown("""
        ### Text-only RAG System
        
        This is a simplified version of the Retrieval-Augmented Generation system that only processes text documents:
        
        - **Text Documents** (TXT, DOCX, PDF)
        
        ### Key Features
        
        1. **Text Processing**: Handles text document ingestion and indexing
        2. **Semantic Search**: Uses embeddings for intelligent retrieval of text content
        3. **Local LLM**: Uses Microsoft's Phi-3 Mini for answer generation
        4. **Offline Operation**: No internet required after initial setup
        5. **Citation Support**: Provides sources for all retrieved information
        
        ### Technology Stack
        
        - **Text Embedding**: sentence-transformers
        - **Vector Database**: FAISS
        - **LLM**: Microsoft Phi-3 Mini
        - **Framework**: Streamlit
        
        ### How It Works
        
        1. **Ingest**: Text documents are processed and converted to embeddings
        2. **Index**: Embeddings are stored in a vector database
        3. **Retrieve**: Queries find similar text embeddings in the database
        4. **Generate**: An LLM generates answers based on retrieved text context
        
        ### Usage Tips
        
        - Upload text documents in the **Text Ingest** tab
        - Ask questions in the **Chat** tab
        - Check system status in the **Status** tab
        """)
        
        st.markdown("### System Information")
        st.text(f"Python Version: {sys.version}")
        st.text(f"Working Directory: {os.getcwd()}")
        
        # Show LLM status
        if 'initialized' in st.session_state and st.session_state.initialized and st.session_state.generator.model is not None:
            st.success("✅ LLM Model: Loaded successfully")
            if hasattr(st.session_state.generator, 'device'):
                st.text(f"Device: {st.session_state.generator.device}")
        else:
            st.warning("⚠️ LLM Model: Not available (using fallback mode)")

if __name__ == "__main__":
    main()