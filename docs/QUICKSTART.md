# 🚀 Quick Start Guide

## Multi-Lingual Product Catalog Translator

### 🎯 Overview
This application helps e-commerce sellers translate their product listings into multiple Indian languages using AI-powered translation.

### ⚡ Quick Setup (5 minutes)

#### Option 1: Automated Setup (Recommended)
Run the setup script:
```bash
# Windows
setup.bat

# Linux/Mac  
./setup.sh
```

#### Option 2: Manual Setup
1. **Install Dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   cd backend
   python -c "from database import DatabaseManager; DatabaseManager().initialize_database()"
   ```

### 🏃‍♂️ Running the Application

#### Option 1: Using VS Code Tasks
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run "Tasks: Run Task"
3. Select "Start Full Application"

#### Option 2: Manual Start
1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   python main.py
   ```
   ✅ Backend running at: http://localhost:8000

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   streamlit run app.py
   ```
   ✅ Frontend running at: http://localhost:8501

### 🌐 Using the Application

1. **Open your browser** → http://localhost:8501
2. **Enter product details**:
   - Product Title (required)
   - Product Description (required) 
   - Category (optional)
3. **Select languages**:
   - Source language (or use auto-detect)
   - Target languages (Hindi, Tamil, etc.)
4. **Click "Translate"**
5. **Review and edit** translations if needed
6. **Submit corrections** to improve the system

### 📊 Key Features

- **🔍 Auto Language Detection** - Automatically detect source language
- **🌍 15+ Indian Languages** - Hindi, Tamil, Telugu, Bengali, and more
- **✏️ Manual Corrections** - Edit translations and provide feedback
- **📈 Analytics** - View translation history and statistics
- **⚡ Batch Processing** - Translate multiple products at once

### 🛠️ Development Mode

The app runs in **development mode** by default with:
- Mock translation service (fast, no GPU needed)
- Sample translations for common phrases
- Full UI functionality for testing

### 🚀 Production Mode

To use actual IndicTrans2 models:
1. Install IndicTrans2:
   ```bash
   pip install git+https://github.com/AI4Bharat/IndicTrans2.git
   ```
2. Update `MODEL_TYPE=indictrans2-1b` in `.env`
3. Ensure GPU availability (recommended)

### 📚 API Documentation

When backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/

### 🔧 Troubleshooting

#### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Install dependencies: `pip install -r backend/requirements.txt`
- Check port 8000 is free

#### Frontend won't start  
- Install Streamlit: `pip install streamlit`
- Check port 8501 is free
- Ensure backend is running first

#### Translation errors
- Backend must be running on port 8000
- Check API health at http://localhost:8000
- Review logs in terminal

### 💡 Next Steps

1. **Try the demo**: Run `python demo.py`
2. **Read full documentation**: Check `README.md`
3. **Explore the code**: Backend in `/backend`, Frontend in `/frontend`
4. **Contribute**: Submit issues and pull requests

### 🤝 Support

- **Documentation**: See `README.md` for detailed information
- **API Reference**: http://localhost:8000/docs (when running)
- **Issues**: Report bugs via GitHub Issues

---
**Happy Translating! 🌟**
