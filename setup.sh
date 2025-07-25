#!/bin/bash

# Multi-Lingual Product Catalog Translator Setup Script
# This script sets up the development environment for the project

echo "🌐 Setting up Multi-Lingual Product Catalog Translator..."
echo "=================================================="

# Check Python version
python_version=$(python --version 2>&1)
echo "📋 Checking Python version: $python_version"

if ! python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "❌ Python 3.9+ is required. Please upgrade Python."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
pip install -r requirements.txt
cd ..

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Copy environment file
echo "⚙️ Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "📝 Please review and modify .env file as needed"
fi

# Initialize database
echo "🗄️ Initializing database..."
cd backend
python -c "
from database import DatabaseManager
db = DatabaseManager()
db.initialize_database()
print('✅ Database initialized successfully')
"
cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Start backend:  cd backend && python main.py"
echo "2. Start frontend: cd frontend && streamlit run app.py"
echo ""
echo "Then open your browser and go to http://localhost:8501"
echo ""
echo "📚 For more information, see README.md"
