#!/usr/bin/env python3
"""
Download script for IndicTrans2 model files
This script downloads the necessary model files for IndicTrans2 translation
"""

import os
import requests
import subprocess
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories for model files"""
    model_dir = Path("models/indictrans2")
    model_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {model_dir}")
    return model_dir

def install_dependencies():
    """Install additional dependencies for IndicTrans2"""
    print("📦 Installing additional dependencies...")
    
    dependencies = [
        "git+https://github.com/anoopkunchukuttan/indic_nlp_library",
        "sentencepiece",
        "sacremoses", 
        "mosestokenizer",
        "ctranslate2",
        "regex",
        "nltk"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Installed {dep}")
            else:
                print(f"⚠️ Warning: Failed to install {dep}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")

def download_nltk_data():
    """Download NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt')
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️ Warning: Failed to download NLTK data: {e}")

def download_model_files(model_dir):
    """Download IndicTrans2 model files"""
    print("🤖 Downloading IndicTrans2 model files...")
    
    # Note: You need to get the actual download URLs for IndicTrans2 models
    # This is a placeholder - check IndicTrans2 documentation for actual URLs
    
    model_urls = {
        # These are example URLs - replace with actual IndicTrans2 model URLs
        "ct2_int8_model": "https://huggingface.co/ai4bharat/indictrans2-indic-en-1B/resolve/main/ct2_int8_model.bin",
        "sentencepiece.model": "https://huggingface.co/ai4bharat/indictrans2-indic-en-1B/resolve/main/sentencepiece.model",
        "config.json": "https://huggingface.co/ai4bharat/indictrans2-indic-en-1B/resolve/main/config.json"
    }
    
    print("⚠️ Note: You need to manually download IndicTrans2 model files")
    print("Please visit: https://github.com/AI4Bharat/IndicTrans2#download-models")
    print(f"And download the model files to: {model_dir}")
    
    # Create placeholder files to indicate where models should go
    readme_content = """# IndicTrans2 Model Files

This directory should contain the IndicTrans2 model files.

To use the real IndicTrans2 model:

1. Visit: https://github.com/AI4Bharat/IndicTrans2#download-models
2. Download the appropriate model files (CTranslate2 format recommended)
3. Place them in this directory
4. Update MODEL_TYPE=indictrans2 in your .env file

Model files typically include:
- model.bin (CTranslate2 model)
- sentencepiece.model (SentencePiece tokenizer)
- config.json (model configuration)
- vocab files

For now, the application will run in mock mode for development.
"""
    
    readme_path = model_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Created {readme_path} with instructions")

def main():
    """Main download function"""
    print("🚀 IndicTrans2 Setup Script")
    print("=" * 50)
    
    # Create directories
    model_dir = create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Download NLTK data
    download_nltk_data()
    
    # Download model files (placeholder for now)
    download_model_files(model_dir)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed!")
    print("\nNext steps:")
    print("1. Follow instructions in models/indictrans2/README.md to download model files")
    print("2. Update MODEL_TYPE=indictrans2 in .env to use real models")
    print("3. Run your application: python backend/main.py")
    print("\nFor now, the app will work in mock mode for development.")

if __name__ == "__main__":
    main()
