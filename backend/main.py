"""
FastAPI backend for Multi-Lingual Product Catalog Translator
Uses IndicTrans2 by AI4Bharat for translation between Indian languages
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import logging
from datetime import datetime

from translation_service import TranslationService
from database import DatabaseManager
from models import (
    LanguageDetectionRequest,
    LanguageDetectionResponse,
    TranslationRequest,
    TranslationResponse,
    CorrectionRequest,
    CorrectionResponse,
    TranslationHistory
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Lingual Catalog Translator",
    description="AI-powered translation service for e-commerce product catalogs using IndicTrans2",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
translation_service = TranslationService()
db_manager = DatabaseManager()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Multi-Lingual Catalog Translator API...")
    db_manager.initialize_database()
    await translation_service.load_models()
    logger.info("API startup complete!")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Multi-Lingual Product Catalog Translator API",
        "status": "healthy",
        "version": "1.0.0",
        "supported_languages": translation_service.get_supported_languages()
    }

@app.post("/detect-language", response_model=LanguageDetectionResponse)
async def detect_language(request: LanguageDetectionRequest):
    """
    Detect the language of input text
    
    Args:
        request: Contains text to analyze
        
    Returns:
        Detected language code and confidence score
    """
    try:
        logger.info(f"Language detection request for text: {request.text[:50]}...")
        
        result = await translation_service.detect_language(request.text)
        
        logger.info(f"Language detected: {result['language']} (confidence: {result['confidence']})")
        
        return LanguageDetectionResponse(
            language=result['language'],
            confidence=result['confidence'],
            language_name=result.get('language_name', result['language'])
        )
        
    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text using IndicTrans2
    
    Args:
        request: Contains text, source and target language codes
        
    Returns:
        Translated text and metadata
    """
    try:
        logger.info(f"Translation request: {request.source_language} -> {request.target_language}")
        
        # Auto-detect source language if not provided
        if not request.source_language:
            detection_result = await translation_service.detect_language(request.text)
            request.source_language = detection_result['language']
            logger.info(f"Auto-detected source language: {request.source_language}")
        
        # Perform translation
        translation_result = await translation_service.translate(
            text=request.text,
            source_lang=request.source_language,
            target_lang=request.target_language
        )
        
        # Store translation in database
        translation_id = db_manager.store_translation(
            original_text=request.text,
            translated_text=translation_result['translated_text'],
            source_language=request.source_language,
            target_language=request.target_language,
            model_confidence=translation_result.get('confidence', 0.0)
        )
        
        logger.info(f"Translation completed. ID: {translation_id}")
        
        return TranslationResponse(
            translated_text=translation_result['translated_text'],
            source_language=request.source_language,
            target_language=request.target_language,
            confidence=translation_result.get('confidence', 0.0),
            translation_id=translation_id
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/submit-correction", response_model=CorrectionResponse)
async def submit_correction(request: CorrectionRequest):
    """
    Submit manual correction for a translation
    
    Args:
        request: Contains translation ID and corrected text
        
    Returns:
        Confirmation of correction submission
    """
    try:
        logger.info(f"Correction submission for translation ID: {request.translation_id}")
        
        # Store correction in database
        correction_id = db_manager.store_correction(
            translation_id=request.translation_id,
            corrected_text=request.corrected_text,
            feedback=request.feedback
        )
        
        logger.info(f"Correction stored with ID: {correction_id}")
        
        return CorrectionResponse(
            correction_id=correction_id,
            message="Correction submitted successfully",
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Correction submission error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit correction: {str(e)}")

@app.get("/history", response_model=List[TranslationHistory])
async def get_translation_history(limit: int = 50, offset: int = 0):
    """
    Get translation history
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of translation history records
    """
    try:
        history = db_manager.get_translation_history(limit=limit, offset=offset)
        return [TranslationHistory(**record) for record in history]
        
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": translation_service.get_supported_languages(),
        "total_count": len(translation_service.get_supported_languages())
    }

@app.post("/batch-translate")
async def batch_translate(texts: List[str], target_language: str, source_language: Optional[str] = None):
    """
    Batch translate multiple texts
    
    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code (auto-detect if not provided)
        
    Returns:
        List of translation results
    """
    try:
        logger.info(f"Batch translation request for {len(texts)} texts")
        
        results = []
        for text in texts:
            # Auto-detect source language if not provided
            if not source_language:
                detection_result = await translation_service.detect_language(text)
                detected_source = detection_result['language']
            else:
                detected_source = source_language
            
            # Perform translation
            translation_result = await translation_service.translate(
                text=text,
                source_lang=detected_source,
                target_lang=target_language
            )
            
            # Store translation in database
            translation_id = db_manager.store_translation(
                original_text=text,
                translated_text=translation_result['translated_text'],
                source_language=detected_source,
                target_language=target_language,
                model_confidence=translation_result.get('confidence', 0.0)
            )
            
            results.append({
                "original_text": text,
                "translated_text": translation_result['translated_text'],
                "source_language": detected_source,
                "target_language": target_language,
                "translation_id": translation_id,
                "confidence": translation_result.get('confidence', 0.0)
            })
        
        logger.info(f"Batch translation completed for {len(results)} texts")
        return {"translations": results}
        
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
