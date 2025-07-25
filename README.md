# 🌐 Multi-Lingual Product Catalog Translator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![IndicTrans2](https://img.shields.io/badge/IndicTrans2-AI4Bharat-orange.svg)](https://github.com/AI4Bharat/IndicTrans2)

A powerful AI-driven web application that helps e-commerce sellers translate their product listings into multiple Indian languages using **IndicTrans2** by AI4Bharat. Built specifically to address language barriers in Indian e-commerce platforms.

## 🎯 Problem Statement

E-commerce sellers often list products in their native languages, creating barriers for buyers from different linguistic backgrounds. This leads to:
- Reduced product discoverability
- Limited customer reach
- Lost sales opportunities
- Poor buyer-seller communication

## 💡 Solution

Our Multi-Lingual Product Catalog Translator provides:
- **Automatic language detection** for input text
- **AI-powered translation** using IndicTrans2 by AI4Bharat
- **Support for 15+ Indian languages** including Hindi, Tamil, Telugu, Bengali, etc.
- **Manual correction interface** for sellers to improve translations
- **Feedback loop system** for continuous improvement
- **Translation history and analytics** for tracking performance

## 🏗️ Architecture

```
User (Seller)
      │
Streamlit UI
      │
FastAPI Backend ←──── SQLite DB
      │
IndicTrans2 API & LangDetect
```

## 🚀 Features

### Core Features
- ✅ **Automatic Language Detection** - Detect source language automatically
- ✅ **Multi-Language Translation** - Support for 15+ Indian languages
- ✅ **Manual Editing Interface** - Easy correction of translations
- ✅ **Batch Translation** - Translate multiple products at once
- ✅ **Translation History** - Track all translations and corrections
- ✅ **Analytics Dashboard** - Insights into translation patterns

### Supported Languages
- **Hindi** (हिंदी)
- **Bengali** (বাংলা)
- **Tamil** (தமிழ்)
- **Telugu** (తెలుగు)
- **Gujarati** (ગુજરાતી)
- **Kannada** (ಕನ್ನಡ)
- **Malayalam** (മലയാളം)
- **Marathi** (मराठी)
- **Punjabi** (ਪੰਜਾਬੀ)
- **Odia** (ଓଡ଼ିଆ)
- **Urdu** (اردو)
- **Assamese** (অসমীয়া)
- **Nepali** (नेपाली)
- **Sanskrit** (संस्कृत)
- **English**

## 📁 Project Structure

```
catalog-translator/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # Pydantic models for API
│   ├── translation_service.py  # IndicTrans2 integration
│   ├── database.py         # SQLite database manager
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit frontend
│   ├── app.py             # Main Streamlit application
│   └── requirements.txt   # Frontend dependencies
├── data/                  # Database and data files
│   └── translations.db    # SQLite database (auto-created)
├── .github/               # GitHub configuration
│   └── copilot-instructions.md
└── README.md              # This file
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Translation Engine** | IndicTrans2 by AI4Bharat | Neural machine translation for Indian languages |
| **Language Detection** | LangDetect / FastText | Automatic source language detection |
| **Backend API** | FastAPI (Python) | High-performance REST API |
| **Frontend UI** | Streamlit | Interactive web interface |
| **Database** | SQLite | Translation storage and history |
| **Deployment** | Hugging Face Spaces | Cloud deployment platform |

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- 8GB+ RAM (recommended for IndicTrans2 models)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BharatMLStack
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   ```

4. **Install IndicTrans2** (Optional - for production)
   ```bash
   pip install git+https://github.com/AI4Bharat/IndicTrans2.git
   ```

### Running the Application

1. **Start the FastAPI backend**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run app.py
   ```
   The web interface will be available at `http://localhost:8501`

3. **Access the application**
   Open your browser and go to `http://localhost:8501`

## 📖 Usage Guide

### For Sellers

1. **Enter Product Details**
   - Add your product title and description
   - Optionally specify the category
   - Choose source language (or use auto-detect)

2. **Select Target Languages**
   - Choose one or more languages to translate to
   - Popular choices: Hindi, English, Tamil, Bengali

3. **Review and Edit Translations**
   - Check the AI-generated translations
   - Make manual corrections if needed
   - Submit corrections to improve the system

4. **Track Your Translations**
   - View translation history
   - Monitor translation quality
   - Analyze language pair performance

### API Usage

The backend provides RESTful APIs for integration:

#### Detect Language
```bash
curl -X POST "http://localhost:8000/detect-language" \
     -H "Content-Type: application/json" \
     -d '{"text": "यह एक अच्छी किताब है।"}'
```

#### Translate Text
```bash
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "यह एक अच्छी किताब है।",
       "source_language": "hi",
       "target_language": "en"
     }'
```

#### Submit Correction
```bash
curl -X POST "http://localhost:8000/submit-correction" \
     -H "Content-Type: application/json" \
     -d '{
       "translation_id": 123,
       "corrected_text": "This is an excellent book.",
       "feedback": "Context-specific improvement"
     }'
```

## 🧪 Development Mode

The application includes a **mock translation service** for development and testing:

- Uses rule-based language detection
- Provides sample translations for common phrases
- Allows full functionality testing without requiring the heavy IndicTrans2 models
- Perfect for development and demonstration

To enable production mode with actual IndicTrans2:
1. Install IndicTrans2: `pip install git+https://github.com/AI4Bharat/IndicTrans2.git`
2. Update the `translation_service.py` to use real models
3. Download the model weights (1.1GB+ for full model)

## 📊 API Documentation

When the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database
DATABASE_PATH=../data/translations.db

# Model Configuration
MODEL_NAME=ai4bharat/indictrans2-indic-en-1B
DEVICE=cuda  # or cpu
```

### Model Selection
- **Development**: Mock translation (fast, no GPU required)
- **Production**: IndicTrans2-1B (best quality, requires GPU)
- **Balanced**: IndicTrans2-Distilled (good quality, faster inference)

## 🚀 Deployment

### Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload your code
3. Add a `requirements.txt` with all dependencies
4. Configure the Space to run Streamlit

### Docker Deployment
```dockerfile
# Example Dockerfile for backend
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Local Production
```bash
# Backend with Gunicorn
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend
cd frontend
streamlit run app.py --server.port 8501
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
pytest
```

### API Testing
```bash
# Test API health
curl http://localhost:8000/

# Test language detection
curl -X POST http://localhost:8000/detect-language \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world"}'
```

## 📈 Performance

### Model Performance
- **IndicTrans2-1B**: BLEU score 35+ on IN22 benchmark
- **Translation Speed**: ~2-5 seconds per sentence (GPU)
- **Supported Text Length**: Up to 512 tokens per request

### System Requirements
- **Minimum**: 4GB RAM, CPU-only (mock mode)
- **Recommended**: 8GB+ RAM, NVIDIA GPU with 6GB+ VRAM
- **Production**: 16GB+ RAM, NVIDIA GPU with 12GB+ VRAM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI4Bharat** for the incredible IndicTrans2 model
- **Meesho** for inspiration and the problem statement
- **FastAPI** and **Streamlit** communities for excellent frameworks
- **Hugging Face** for model hosting and deployment platform

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Documentation**: Full API documentation available at `/docs` endpoint

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Basic translation functionality
- ✅ Web interface
- ✅ Manual correction system
- ✅ Translation history

### Phase 2 (Next)
- 🔄 Real IndicTrans2 integration
- 🔄 Batch file upload
- 🔄 Advanced analytics
- 🔄 User authentication

### Phase 3 (Future)
- 📋 API rate limiting
- 📋 Model fine-tuning with corrections
- 📋 Multi-tenant support
- 📋 Mobile responsive design

---

**Built with ❤️ for the Indian e-commerce ecosystem**
