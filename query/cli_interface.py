"""
CLI interface for the multimodal RAG system.
"""

import argparse
import logging
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CLIInterface:
    """Command-line interface for the RAG system."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description="Multimodal Retrieval-Augmented Generation System"
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Ingest command
        ingest_parser = subparsers.add_parser('ingest', help='Ingest documents into the system')
        ingest_parser.add_argument('--input_dir', required=True, 
                                  help='Directory containing files to ingest')
        ingest_parser.add_argument('--recursive', action='store_true',
                                  help='Process subdirectories recursively')
        
        # Query command
        query_parser = subparsers.add_parser('query', help='Query the system')
        query_parser.add_argument('--question', required=True, 
                                 help='Question to ask the system')
        query_parser.add_argument('--mode', choices=['text', 'image', 'hybrid'], 
                                 default='text', help='Query mode')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        
        return parser
    
    def run(self, args: List[str] = None):
        """
        Run the CLI interface.
        
        Args:
            args: Command line arguments (optional)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            if parsed_args.command == 'ingest':
                self._handle_ingest(parsed_args)
            elif parsed_args.command == 'query':
                self._handle_query(parsed_args)
            elif parsed_args.command == 'status':
                self._handle_status(parsed_args)
            else:
                self.parser.print_help()
        except Exception as e:
            logger.error(f"Error running CLI: {str(e)}")
            print(f"Error: {str(e)}")
    
    def _handle_ingest(self, args):
        """Handle ingest command."""
        print(f"Ingesting documents from: {args.input_dir}")
        if args.recursive:
            print("Processing recursively")
        
        # Import here to avoid circular imports
        from ingestion.ingestor import Ingestor
        from utils.config import config
        
        try:
            ingestor = Ingestor()
            processed_count = ingestor.ingest_directory(args.input_dir, args.recursive)
            print(f"Successfully ingested {processed_count} files")
        except Exception as e:
            logger.error(f"Error during ingestion: {str(e)}")
            print(f"Error during ingestion: {str(e)}")
    
    def _handle_query(self, args):
        """Handle query command."""
        print(f"Processing query: {args.question}")
        print(f"Query mode: {args.mode}")
        
        # Import here to avoid circular imports
        from retrieval.retriever import Retriever
        from generation.generator import Generator
        from indexing.vector_store import VectorStore
        from embedding.text_embedder import TextEmbedder
        from embedding.image_embedder import ImageEmbedder
        from utils.config import config
        
        try:
            # Initialize components
            vector_store = VectorStore(
                dimension=config.get('models.text_embedding.dim', 384),
                index_path=config.get('vector_db.index_path'),
                metadata_path=config.get('vector_db.metadata_path')
            )
            
            text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
            image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
            retriever = Retriever(vector_store, text_embedder, image_embedder)
            generator = Generator(
                model_name=config.get('models.llm.name'),
                max_tokens=config.get('models.llm.max_tokens', 2048)
            )
            
            # Retrieve context
            if args.mode == 'image':
                # For image mode, we'd need an image path - not implemented in this CLI version
                context = []
            else:
                context = retriever.retrieve_text(args.question, k=config.get('retrieval.top_k', 5))
            
            # Generate answer
            if context:
                answer = generator.generate_answer(args.question, context)
                print("\nAnswer:")
                print(answer)
                print("\nSources:")
                self._print_citations(context)
            else:
                print("No relevant context found for your query.")
        except Exception as e:
            logger.error(f"Error during query processing: {str(e)}")
            print(f"Error during query processing: {str(e)}")
    
    def _handle_status(self, args):
        """Handle status command."""
        print("System Status:")
        
        # Import here to avoid circular imports
        from indexing.vector_store import VectorStore
        from utils.config import config
        
        try:
            vector_store = VectorStore(
                dimension=config.get('models.text_embedding.dim', 384),
                index_path=config.get('vector_db.index_path'),
                metadata_path=config.get('vector_db.metadata_path')
            )
            
            total_vectors = vector_store.get_total_vectors()
            print(f"  Indexed vectors: {total_vectors}")
            print(f"  Index path: {config.get('vector_db.index_path')}")
            print(f"  Metadata path: {config.get('vector_db.metadata_path')}")
        except Exception as e:
            logger.error(f"Error retrieving status: {str(e)}")
            print(f"Error retrieving status: {str(e)}")
    
    def _print_citations(self, context: List[Dict[str, Any]]):
        """
        Print citations for retrieved context.
        
        Args:
            context: Retrieved context items
        """
        for i, item in enumerate(context, 1):
            source = item.get('source', 'Unknown')
            item_type = item.get('type', 'unknown')
            
            if item_type == 'text':
                page = item.get('page', '')
                paragraph = item.get('paragraph', '')
                citation = f"[{i}] {source}"
                if page or paragraph:
                    details = []
                    if page:
                        details.append(f"Page {page}")
                    if paragraph:
                        details.append(f"Paragraph {paragraph}")
                    citation += f" ({', '.join(details)})"
                print(citation)
            elif item_type == 'image':
                print(f"[{i}] Image: {source}")
            elif item_type == 'audio':
                print(f"[{i}] Audio: {source}")