#!/usr/bin/env python3
"""
Main entry point for the multimodal RAG system.
"""

import sys
import os
import logging
import argparse

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
from utils.logger import setup_logger
logger = setup_logger("multimodal_rag_main")

def main():
    """Main entry point."""
    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description="Multimodal RAG System")
        parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
        args, unknown = parser.parse_known_args()
        
        if args.gui:
            # Import and run GUI interface
            from query.gui_interface import GUIInterface
            gui = GUIInterface()
            gui.run()
        else:
            # Import CLI interface
            from query.cli_interface import CLIInterface
            
            # Create and run CLI with all arguments
            cli = CLIInterface()
            cli.run(sys.argv[1:])
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()