@echo off
REM Multi-Lingual Product Catalog Translator Setup Script (Windows)
REM This script sets up the development environment for the project

echo 🌐 Setting up Multi-Lingual Product Catalog Translator...
echo ==================================================

REM Check Python version
echo 📋 Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.9+
    pause
    exit /b 1
)

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
pip install -r requirements.txt
cd ..

REM Create data directory
echo 📁 Creating data directory...
if not exist "data" mkdir data

REM Copy environment file
echo ⚙️ Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo ✅ Created .env file from .env.example
    echo 📝 Please review and modify .env file as needed
)

REM Initialize database
echo 🗄️ Initializing database...
cd backend
python -c "from database import DatabaseManager; db = DatabaseManager(); db.initialize_database(); print('✅ Database initialized successfully')"
cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo To start the application:
echo 1. Start backend:  cd backend ^&^& python main.py
echo 2. Start frontend: cd frontend ^&^& streamlit run app.py
echo.
echo Then open your browser and go to http://localhost:8501
echo.
echo 📚 For more information, see README.md

pause
