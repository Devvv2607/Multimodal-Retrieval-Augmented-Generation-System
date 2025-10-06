"""
Comprehensive diagnostic script to identify issues in the RAG system.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def comprehensive_diagnostic():
    """Run comprehensive diagnostics on the RAG system."""
    print("Comprehensive RAG System Diagnostic")
    print("=" * 40)
    
    # 1. Check current working directory
    print("1. Current Working Directory:")
    cwd = os.getcwd()
    print(f"   {cwd}")
    
    # 2. Check if we're in the right directory
    expected_files = ['main.py', 'config.yaml', 'streamlit_app.py']
    print("\n2. Required Files Check:")
    for file in expected_files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"   {status} {file}: {'Found' if exists else 'Missing'}")
    
    # 3. Check data directory and files
    print("\n3. Data Directory Check:")
    data_dir = "./data"
    if os.path.exists(data_dir):
        print(f"   ✓ Data directory exists: {data_dir}")
        try:
            files = os.listdir(data_dir)
            print(f"   Files in data directory: {files}")
            
            # Check specific files
            index_file = os.path.join(data_dir, "index.faiss")
            metadata_file = os.path.join(data_dir, "metadata.json")
            
            index_exists = os.path.exists(index_file)
            metadata_exists = os.path.exists(metadata_file)
            
            print(f"   Index file: {'✓ Found' if index_exists else '✗ Missing'}")
            print(f"   Metadata file: {'✓ Found' if metadata_exists else '✗ Missing'}")
            
            if index_exists:
                size = os.path.getsize(index_file)
                print(f"   Index file size: {size} bytes")
                
            if metadata_exists:
                size = os.path.getsize(metadata_file)
                print(f"   Metadata file size: {size} bytes")
                
                # Try to read and parse metadata
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    print(f"   Metadata entries: {len(metadata)}")
                    if metadata:
                        print("   Sample entry:")
                        sample = metadata[0] if metadata else {}
                        for key, value in list(sample.items())[:3]:  # Show first 3 items
                            print(f"     {key}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
                except Exception as e:
                    print(f"   Error reading metadata: {e}")
                    
        except Exception as e:
            print(f"   Error accessing data directory: {e}")
    else:
        print(f"   ✗ Data directory does not exist: {data_dir}")
    
    # 4. Check configuration
    print("\n4. Configuration Check:")
    try:
        from utils.config import config
        print("   ✓ Configuration loaded successfully")
        
        # Check key configuration values
        config_items = [
            ('vector_db.index_path', 'Vector DB Index Path'),
            ('vector_db.metadata_path', 'Vector DB Metadata Path'),
            ('models.text_embedding.name', 'Text Embedding Model'),
            ('models.llm.name', 'LLM Model')
        ]
        
        for key, description in config_items:
            value = config.get(key, 'NOT SET')
            print(f"   {description}: {value}")
            
    except Exception as e:
        print(f"   ✗ Error loading configuration: {e}")
    
    # 5. Test component imports
    print("\n5. Component Import Test:")
    components = [
        ('utils.config', 'Config'),
        ('ingestion.ingestor', 'Ingestor'),
        ('embedding.text_embedder', 'TextEmbedder'),
        ('embedding.image_embedder', 'ImageEmbedder'),
        ('indexing.vector_store', 'VectorStore'),
        ('retrieval.retriever', 'Retriever'),
        ('generation.generator', 'Generator')
    ]
    
    for module, name in components:
        try:
            __import__(module)
            print(f"   ✓ {name}: Import successful")
        except Exception as e:
            print(f"   ✗ {name}: Import failed - {e}")
    
    # 6. Test vector store initialization
    print("\n6. Vector Store Test:")
    try:
        from indexing.vector_store import VectorStore
        from utils.config import config
        
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        total_vectors = vector_store.get_total_vectors()
        print(f"   ✓ Vector store initialized successfully")
        print(f"   Total vectors: {total_vectors}")
        
    except Exception as e:
        print(f"   ✗ Vector store initialization failed: {e}")
    
    # 7. Test retrieval
    print("\n7. Retrieval Test:")
    try:
        from retrieval.retriever import Retriever
        from embedding.text_embedder import TextEmbedder
        from embedding.image_embedder import ImageEmbedder
        
        # Initialize components
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
        retriever = Retriever(vector_store, text_embedder, image_embedder)
        
        print("   ✓ Retriever initialized successfully")
        
        # Test a simple query
        if vector_store.get_total_vectors() > 0:
            test_query = "test query"
            results = retriever.retrieve_text(test_query, k=1)
            print(f"   Test query '{test_query}' returned {len(results)} results")
        else:
            print("   ⚠️  No vectors to test retrieval")
            
    except Exception as e:
        print(f"   ✗ Retrieval test failed: {e}")
    
    # 8. Test generator
    print("\n8. Generator Test:")
    try:
        from generation.generator import Generator
        
        generator = Generator(
            model_name=config.get('models.llm.name'),
            max_tokens=config.get('models.llm.max_tokens', 2048)
        )
        
        print("   ✓ Generator initialized successfully")
        if generator.model is not None:
            print("   ✓ LLM model loaded successfully")
        else:
            print("   ⚠️  LLM model not loaded (fallback mode)")
            
    except Exception as e:
        print(f"   ✗ Generator test failed: {e}")
    
    print("\n" + "=" * 40)
    print("Diagnostic complete!")

if __name__ == "__main__":
    comprehensive_diagnostic()