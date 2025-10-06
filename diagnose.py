"""
Diagnostic script to check the system status.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def diagnose_system():
    """Diagnose the system status."""
    print("Multimodal RAG System Diagnosis")
    print("=" * 35)
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    expected_files = ['main.py', 'config.yaml', 'streamlit_app.py']
    found_files = []
    missing_files = []
    
    for file in expected_files:
        if os.path.exists(file):
            found_files.append(file)
        else:
            missing_files.append(file)
    
    print(f"\nFound files: {found_files}")
    if missing_files:
        print(f"Missing files: {missing_files}")
    
    # Check data directory
    data_dir = "./data"
    if os.path.exists(data_dir):
        print(f"\nData directory exists: {data_dir}")
        try:
            files = os.listdir(data_dir)
            print(f"Files in data directory: {files}")
            
            # Check for index and metadata files
            index_file = os.path.join(data_dir, "index.faiss")
            metadata_file = os.path.join(data_dir, "metadata.json")
            
            if os.path.exists(index_file):
                print(f"✓ Index file found: {index_file}")
                # Get file size
                size = os.path.getsize(index_file)
                print(f"  Index file size: {size} bytes")
            else:
                print(f"✗ Index file not found: {index_file}")
                
            if os.path.exists(metadata_file):
                print(f"✓ Metadata file found: {metadata_file}")
                # Get file size
                size = os.path.getsize(metadata_file)
                print(f"  Metadata file size: {size} bytes")
                
                # Try to load metadata
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    print(f"  Metadata entries: {len(metadata)}")
                    if metadata:
                        print("  Sample metadata entry:")
                        print(f"    {metadata[0]}")
                except Exception as e:
                    print(f"  Error reading metadata: {e}")
            else:
                print(f"✗ Metadata file not found: {metadata_file}")
        except Exception as e:
            print(f"Error accessing data directory: {e}")
    else:
        print(f"\n✗ Data directory does not exist: {data_dir}")
    
    # Check configuration
    try:
        from utils.config import config
        print("\n✓ Configuration loaded successfully")
        print(f"  Vector DB index path: {config.get('vector_db.index_path')}")
        print(f"  Vector DB metadata path: {config.get('vector_db.metadata_path')}")
    except Exception as e:
        print(f"\n✗ Error loading configuration: {e}")
    
    # Check if virtual environment is active
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        print(f"\n✓ Virtual environment active: {venv}")
    else:
        print(f"\n⚠️  Virtual environment not active")

if __name__ == "__main__":
    diagnose_system()