"""
Script to download and setup required models for the multimodal RAG system.
"""

import os
import logging
from transformers import AutoModel, AutoTokenizer
import sentence_transformers
import clip
import whisper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_text_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Download and setup text embedding model.
    
    Args:
        model_name: Name of the sentence transformer model
    """
    try:
        logger.info(f"Setting up text embedding model: {model_name}")
        model = sentence_transformers.SentenceTransformer(model_name)
        logger.info(f"Successfully set up text embedding model: {model_name}")
    except Exception as e:
        logger.error(f"Error setting up text embedding model {model_name}: {str(e)}")
        raise

def setup_clip_model(model_name: str = "ViT-B/32"):
    """
    Download and setup CLIP model.
    
    Args:
        model_name: Name of the CLIP model
    """
    try:
        logger.info(f"Setting up CLIP model: {model_name}")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load(model_name, device=device)
        logger.info(f"Successfully set up CLIP model: {model_name}")
    except Exception as e:
        logger.error(f"Error setting up CLIP model {model_name}: {str(e)}")
        raise

def setup_whisper_model(model_name: str = "base"):
    """
    Download and setup Whisper model.
    
    Args:
        model_name: Name of the Whisper model
    """
    try:
        logger.info(f"Setting up Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        logger.info(f"Successfully set up Whisper model: {model_name}")
    except Exception as e:
        logger.error(f"Error setting up Whisper model {model_name}: {str(e)}")
        raise

def setup_phi3_model(model_name: str = "microsoft/phi-3-mini-4k-instruct"):
    """
    Download and setup Phi-3 model.
    
    Args:
        model_name: Name of the Phi-3 model
    """
    try:
        logger.info(f"Setting up Phi-3 model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        logger.info(f"Successfully set up Phi-3 model: {model_name}")
    except Exception as e:
        logger.error(f"Error setting up Phi-3 model {model_name}: {str(e)}")
        raise

def setup_all_models():
    """Setup all required models for the RAG system."""
    logger.info("Setting up all models for the multimodal RAG system")
    
    try:
        # Setup text embedding model
        setup_text_embedding_model("all-MiniLM-L6-v2")
        
        # Setup CLIP model
        setup_clip_model("ViT-B/32")
        
        # Setup Whisper model
        setup_whisper_model("base")
        
        # Setup Phi-3 model
        setup_phi3_model("microsoft/phi-3-mini-4k-instruct")
        
        logger.info("All models successfully set up!")
    except Exception as e:
        logger.error(f"Error setting up models: {str(e)}")
        raise

if __name__ == "__main__":
    # Import torch here to avoid import issues
    import torch
    setup_all_models()