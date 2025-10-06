"""
Diagnostic script for Streamlit Cloud deployment.
This script helps identify issues with Streamlit Cloud deployment.
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

def check_python_version():
    """Check Python version."""
    st.subheader("Python Version")
    version = sys.version
    st.info(f"Python Version: {version}")
    logger.info(f"Python Version: {version}")
    
    # Check if version is compatible
    version_info = sys.version_info
    if version_info.major >= 3 and version_info.minor >= 8:
        st.success("✅ Python version is compatible")
        return True
    else:
        st.error("❌ Python version is not compatible (requires 3.8+)")
        return False

def check_working_directory():
    """Check working directory."""
    st.subheader("Working Directory")
    cwd = os.getcwd()
    st.info(f"Current Working Directory: {cwd}")
    logger.info(f"Current Working Directory: {cwd}")
    
    # List files in directory
    try:
        files = os.listdir(cwd)
        st.info("Files in directory:")
        for file in files:
            st.text(f"  - {file}")
    except Exception as e:
        st.error(f"Error listing directory: {e}")
        return False
    
    return True

def check_required_files():
    """Check for required files."""
    st.subheader("Required Files")
    
    required_files = [
        "streamlit_app.py",
        "config.yaml",
        "requirements.txt"
    ]
    
    all_found = True
    for file in required_files:
        if os.path.exists(file):
            st.success(f"✅ {file} found")
        else:
            st.error(f"❌ {file} not found")
            all_found = False
    
    return all_found

def check_imports():
    """Check if imports work."""
    st.subheader("Import Checks")
    
    # Core imports
    core_imports = [
        ("streamlit", "streamlit"),
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss"),
        ("numpy", "numpy"),
        ("PIL", "pillow"),
        ("docx", "python-docx"),
        ("PyPDF2", "pypdf2"),
        ("yaml", "pyyaml")
    ]
    
    all_passed = True
    for import_name, package_name in core_imports:
        try:
            __import__(import_name)
            st.success(f"✅ {package_name} ({import_name}) imported successfully")
            logger.info(f"✅ {import_name} imported successfully")
        except ImportError as e:
            st.error(f"❌ {package_name} ({import_name}) import failed: {e}")
            logger.error(f"❌ {import_name} import failed: {e}")
            all_passed = False
        except Exception as e:
            st.warning(f"⚠ {package_name} ({import_name}) import issue: {e}")
            logger.warning(f"⚠ {import_name} import issue: {e}")
    
    return all_passed

def check_project_imports():
    """Check if project-specific imports work."""
    st.subheader("Project-Specific Import Checks")
    
    project_imports = [
        ("ingestion.ingestor", "Ingestor"),
        ("retrieval.retriever", "Retriever"),
        ("generation.generator", "Generator"),
        ("indexing.vector_store", "VectorStore"),
        ("embedding.text_embedder", "TextEmbedder"),
        ("utils.config", "config")
    ]
    
    all_passed = True
    for module_path, class_name in project_imports:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            st.success(f"✅ {module_path}.{class_name} imported successfully")
            logger.info(f"✅ {module_path}.{class_name} imported successfully")
        except ImportError as e:
            st.error(f"❌ {module_path}.{class_name} import failed: {e}")
            logger.error(f"❌ {module_path}.{class_name} import failed: {e}")
            all_passed = False
        except Exception as e:
            st.warning(f"⚠ {module_path}.{class_name} import issue: {e}")
            logger.warning(f"⚠ {module_path}.{class_name} import issue: {e}")
    
    return all_passed

def check_config():
    """Check configuration."""
    st.subheader("Configuration Check")
    
    try:
        from utils.config import config
        
        # Try to access some config values
        text_embedding = config.get('models.text_embedding.name')
        llm_name = config.get('models.llm.name')
        
        st.success("✅ Configuration loaded successfully")
        st.info(f"Text Embedding Model: {text_embedding}")
        st.info(f"LLM Model: {llm_name}")
        
        logger.info("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        st.error(f"❌ Configuration check failed: {e}")
        logger.error(f"❌ Configuration check failed: {e}")
        return False

def check_environment():
    """Check environment variables."""
    st.subheader("Environment Variables")
    
    important_vars = [
        "PYTHONPATH",
        "MODEL_CACHE_DIR"
    ]
    
    for var in important_vars:
        value = os.environ.get(var, "Not set")
        st.info(f"{var}: {value}")

def main():
    """Main diagnostic function."""
    st.set_page_config(
        page_title="Streamlit Cloud Diagnostic",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Streamlit Cloud Diagnostic Tool")
    st.markdown("""
    This tool helps diagnose issues with Streamlit Cloud deployment.
    
    Run this tool on Streamlit Cloud to identify potential issues with your deployment.
    """)
    
    # Run all checks
    with st.spinner("Running diagnostics..."):
        checks = [
            ("Python Version", check_python_version),
            ("Working Directory", check_working_directory),
            ("Required Files", check_required_files),
            ("Package Imports", check_imports),
            ("Project Imports", check_project_imports),
            ("Configuration", check_config),
            ("Environment", check_environment)
        ]
        
        results = []
        for check_name, check_func in checks:
            try:
                st.markdown(f"---")
                result = check_func()
                results.append((check_name, result))
            except Exception as e:
                st.error(f"Error running {check_name}: {e}")
                results.append((check_name, False))
        
        # Show summary
        st.markdown("---")
        st.header("Diagnostic Summary")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        st.info(f"Checks passed: {passed}/{total}")
        
        if passed == total:
            st.success("🎉 All diagnostics passed! Your app should work correctly.")
            st.info("If you're still experiencing issues, check the Streamlit Cloud build logs for specific error messages.")
        else:
            st.warning("⚠ Some diagnostics failed. Please review the issues above.")
            st.info("For detailed troubleshooting, see STREAMLIT_CLOUD_TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()