"""
Simple deployment script for the Multimodal RAG System.
This script provides an easy way to deploy the application locally or to cloud platforms.
"""

import os
import sys
import subprocess
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version {version.major}.{version.minor}.{version.minor} is compatible")
    return True

def run_command(command, shell=False):
    """Run a shell command and return the result."""
    try:
        logger.info(f"Running command: {command}")
        result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
        logger.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with error: {e.stderr}")
        return False

def create_virtual_environment(env_name="rag_env"):
    """Create a virtual environment."""
    logger.info(f"Creating virtual environment: {env_name}")
    if os.name == 'nt':  # Windows
        return run_command(f"python -m venv {env_name}")
    else:  # Unix/Linux/Mac
        return run_command(f"python3 -m venv {env_name}")

def activate_virtual_environment(env_name="rag_env"):
    """Activate the virtual environment."""
    logger.info(f"Activating virtual environment: {env_name}")
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(env_name, "Scripts", "activate")
        return f"{activate_script} && "
    else:  # Unix/Linux/Mac
        activate_script = os.path.join(env_name, "bin", "activate")
        return f"source {activate_script} && "

def install_requirements(requirements_file="requirements.txt"):
    """Install requirements from a file."""
    logger.info(f"Installing requirements from {requirements_file}")
    return run_command(f"pip install -r {requirements_file}")

def install_additional_packages():
    """Install additional packages needed for the application."""
    logger.info("Installing additional packages")
    packages = [
        "git+https://github.com/openai/CLIP.git",
        "streamlit"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}"):
            return False
    return True

def initialize_system():
    """Initialize the system."""
    logger.info("Initializing the system")
    return run_command("python init.py")

def run_streamlit_app():
    """Run the Streamlit application."""
    logger.info("Starting Streamlit application")
    return run_command("streamlit run streamlit_app.py", shell=True)

def deploy_local():
    """Deploy the application locally."""
    logger.info("Starting local deployment")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        logger.error("Failed to create virtual environment")
        return False
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        # On Windows, we need to run commands in the same shell
        commands = [
            "python -m venv rag_env",
            "rag_env\\Scripts\\activate",
            "pip install -r requirements.txt",
            "pip install git+https://github.com/openai/CLIP.git",
            "pip install streamlit",
            "python init.py"
        ]
        
        full_command = " && ".join(commands)
        if not run_command(full_command, shell=True):
            return False
    else:  # Unix/Linux/Mac
        if not install_requirements():
            logger.error("Failed to install requirements")
            return False
        
        if not install_additional_packages():
            logger.error("Failed to install additional packages")
            return False
        
        if not initialize_system():
            logger.error("Failed to initialize system")
            return False
    
    logger.info("Local deployment completed successfully!")
    logger.info("You can now run the application with: streamlit run streamlit_app.py")
    return True

def deploy_streamlit_cloud():
    """Prepare for Streamlit Cloud deployment."""
    logger.info("Preparing for Streamlit Cloud deployment")
    
    # For Streamlit Cloud, we just need to ensure requirements_streamlit.txt is correct
    logger.info("Streamlit Cloud deployment uses requirements_streamlit.txt")
    logger.info("Make sure to set your GitHub repository to use this file")
    
    # Run the setup script for Streamlit Cloud
    logger.info("Running Streamlit Cloud setup")
    return run_command("python setup_deploy.py --streamlit-cloud")

def deploy_docker():
    """Create Docker deployment files."""
    logger.info("Creating Docker deployment files")
    
    # Create Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install CLIP
RUN pip install git+https://github.com/openai/CLIP.git

# Install Streamlit
RUN pip install streamlit

COPY . .

# Initialize the system
RUN python init.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Create docker-compose.yml
    compose_content = """version: '3.8'
services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - MODEL_CACHE_DIR=/app/models/cache
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    logger.info("Docker deployment files created successfully!")
    logger.info("Build with: docker build -t multimodal-rag .")
    logger.info("Run with: docker run -p 8501:8501 multimodal-rag")
    return True

def main():
    """Main function to handle deployment options."""
    parser = argparse.ArgumentParser(description="Deploy the Multimodal RAG System")
    parser.add_argument("--local", action="store_true", help="Deploy locally")
    parser.add_argument("--streamlit-cloud", action="store_true", help="Prepare for Streamlit Cloud deployment")
    parser.add_argument("--docker", action="store_true", help="Create Docker deployment files")
    parser.add_argument("--run", action="store_true", help="Run the Streamlit application after deployment")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any([args.local, args.streamlit_cloud, args.docker]):
        parser.print_help()
        return
    
    success = True
    
    # Handle deployment options
    if args.local:
        success = deploy_local()
    
    if args.streamlit_cloud:
        success = deploy_streamlit_cloud()
    
    if args.docker:
        success = deploy_docker()
    
    # Run the application if requested
    if args.run and success:
        if not run_streamlit_app():
            logger.error("Failed to run Streamlit application")
            success = False
    
    if success:
        logger.info("Deployment completed successfully!")
        if args.run:
            logger.info("Streamlit application is now running")
        else:
            logger.info("You can now run the application with: streamlit run streamlit_app.py")
    else:
        logger.error("Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()