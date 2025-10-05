"""
Initialization script for the multimodal RAG system.
"""

import os
import logging
from utils.logger import setup_logger

logger = setup_logger("multimodal_rag_init")

def create_directories():
    """Create required directories for the system."""
    directories = [
        "./data",
        "./logs",
        "./temp",
        "./input",
        "./output"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {str(e)}")

def initialize_system():
    """Initialize the multimodal RAG system."""
    logger.info("Initializing multimodal RAG system...")
    
    # Create directories
    create_directories()
    
    logger.info("System initialization complete!")

if __name__ == "__main__":
    initialize_system()