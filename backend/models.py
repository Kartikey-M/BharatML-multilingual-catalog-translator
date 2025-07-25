"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LanguageDetectionRequest(BaseModel):
    """Request model for language detection"""
    text: str = Field(..., description="Text to detect language for", min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "text": "यह एक अच्छी किताब है।"
            }
        }

class LanguageDetectionResponse(BaseModel):
    """Response model for language detection"""
    language: str = Field(..., description="Detected language code (e.g., 'hi', 'en')")
    confidence: float = Field(..., description="Confidence score between 0 and 1")
    language_name: str = Field(..., description="Human-readable language name")
    
    class Config:
        schema_extra = {
            "example": {
                "language": "hi",
                "confidence": 0.95,
                "language_name": "Hindi"
            }
        }

class TranslationRequest(BaseModel):
    """Request model for translation"""
    text: str = Field(..., description="Text to translate", min_length=1)
    target_language: str = Field(..., description="Target language code")
    source_language: Optional[str] = Field(None, description="Source language code (auto-detect if not provided)")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "यह एक अच्छी किताब है।",
                "target_language": "en",
                "source_language": "hi"
            }
        }

class TranslationResponse(BaseModel):
    """Response model for translation"""
    translated_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    confidence: float = Field(..., description="Translation confidence score")
    translation_id: int = Field(..., description="Unique translation ID for future reference")
    
    class Config:
        schema_extra = {
            "example": {
                "translated_text": "This is a good book.",
                "source_language": "hi",
                "target_language": "en",
                "confidence": 0.92,
                "translation_id": 12345
            }
        }

class CorrectionRequest(BaseModel):
    """Request model for submitting translation corrections"""
    translation_id: int = Field(..., description="ID of the translation to correct")
    corrected_text: str = Field(..., description="Manually corrected translation", min_length=1)
    feedback: Optional[str] = Field(None, description="Optional feedback about the correction")
    
    class Config:
        schema_extra = {
            "example": {
                "translation_id": 12345,
                "corrected_text": "This is an excellent book.",
                "feedback": "The word 'अच्छी' should be translated as 'excellent' not 'good' in this context"
            }
        }

class CorrectionResponse(BaseModel):
    """Response model for correction submission"""
    correction_id: int = Field(..., description="Unique correction ID")
    message: str = Field(..., description="Success message")
    status: str = Field(..., description="Status of the correction submission")
    
    class Config:
        schema_extra = {
            "example": {
                "correction_id": 67890,
                "message": "Correction submitted successfully",
                "status": "success"
            }
        }

class TranslationHistory(BaseModel):
    """Model for translation history records"""
    id: int = Field(..., description="Translation ID")
    original_text: str = Field(..., description="Original text")
    translated_text: str = Field(..., description="Machine-translated text")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    model_confidence: float = Field(..., description="Model confidence score")
    created_at: datetime = Field(..., description="Timestamp when translation was created")
    corrected_text: Optional[str] = Field(None, description="Manual correction if available")
    correction_feedback: Optional[str] = Field(None, description="Feedback for the correction")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 12345,
                "original_text": "यह एक अच्छी किताब है।",
                "translated_text": "This is a good book.",
                "source_language": "hi",
                "target_language": "en",
                "model_confidence": 0.92,
                "created_at": "2025-01-25T10:30:00Z",
                "corrected_text": "This is an excellent book.",
                "correction_feedback": "Context-specific improvement"
            }
        }

class BatchTranslationRequest(BaseModel):
    """Request model for batch translation"""
    texts: List[str] = Field(..., description="List of texts to translate", min_items=1)
    target_language: str = Field(..., description="Target language code")
    source_language: Optional[str] = Field(None, description="Source language code (auto-detect if not provided)")
    
    class Config:
        schema_extra = {
            "example": {
                "texts": [
                    "यह एक अच्छी किताब है।",
                    "मुझे यह पसंद है।",
                    "कितना पैसा लगेगा?"
                ],
                "target_language": "en",
                "source_language": "hi"
            }
        }

class ProductCatalogItem(BaseModel):
    """Model for e-commerce product catalog items"""
    title: str = Field(..., description="Product title", min_length=1)
    description: str = Field(..., description="Product description", min_length=1)
    category: Optional[str] = Field(None, description="Product category")
    price: Optional[str] = Field(None, description="Product price")
    seller_id: Optional[str] = Field(None, description="Seller identifier")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "शुद्ध कपास की साड़ी",
                "description": "यह एक सुंदर पारंपरिक साड़ी है जो शुद्ध कपास से बनी है। विशेष अवसरों के लिए आदर्श।",
                "category": "वस्त्र",
                "price": "₹2500",
                "seller_id": "seller_123"
            }
        }

class TranslatedProductCatalogItem(BaseModel):
    """Model for translated product catalog items"""
    original_item: ProductCatalogItem
    translated_title: str
    translated_description: str
    translated_category: Optional[str] = None
    source_language: str
    target_language: str
    translation_ids: dict = Field(..., description="Map of field names to translation IDs")
    
    class Config:
        schema_extra = {
            "example": {
                "original_item": {
                    "title": "शुद्ध कपास की साड़ी",
                    "description": "यह एक सुंदर पारंपरिक साड़ी है।",
                    "category": "वस्त्र"
                },
                "translated_title": "Pure Cotton Saree",
                "translated_description": "This is a beautiful traditional saree.",
                "translated_category": "Clothing",
                "source_language": "hi",
                "target_language": "en",
                "translation_ids": {
                    "title": 12345,
                    "description": 12346,
                    "category": 12347
                }
            }
        }

# Language mapping for Indian languages supported by IndicTrans2
SUPPORTED_LANGUAGES = {
    "as": "Assamese",
    "bn": "Bengali", 
    "brx": "Bodo",
    "doi": "Dogri",
    "en": "English",
    "gom": "Goan Konkani",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kha": "Khasi",
    "kn": "Kannada",
    "kok": "Konkani",
    "ks": "Kashmiri (Arabic)",
    "ks_Deva": "Kashmiri (Devanagari)", 
    "lus": "Lushai",
    "mai": "Maithili",
    "ml": "Malayalam",
    "mni": "Manipuri (Bengali)",
    "mni_Mtei": "Manipuri (Meetei Mayek)",
    "mr": "Marathi",
    "ne": "Nepali",
    "or": "Odia",
    "pa": "Punjabi",
    "sa": "Sanskrit",
    "sat": "Santali (Ol Chiki)",
    "sat_Deva": "Santali (Devanagari)",
    "sd": "Sindhi (Arabic)",
    "sd_Deva": "Sindhi (Devanagari)",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu"
}
