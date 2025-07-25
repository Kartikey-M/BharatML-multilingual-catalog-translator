"""
Translation service using IndicTrans2 by AI4Bharat
Handles language detection and translation between Indian languages
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
try:
    import fasttext
    FASTTEXT_AVAILABLE = True
except ImportError:
    FASTTEXT_AVAILABLE = False
    fasttext = None
import os
import requests
from dotenv import load_dotenv
from models import SUPPORTED_LANGUAGES

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# --- Model Configuration ---
MODEL_TYPE = os.getenv("MODEL_TYPE", "mock") # "mock" or "indictrans2"
FASTTEXT_MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
FASTTEXT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "lid.176.bin")


class TranslationService:
    """Service for handling language detection and translation using IndicTrans2"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.language_detector = None
        self.device = "cuda" if torch.cuda.is_available() and os.getenv("DEVICE", "cuda") == "cuda" else "cpu"
        self.model_name = os.getenv("MODEL_NAME", "ai4bharat/indictrans2-indic-en-1B")
        self.model_loaded = False
        
        # Language code mappings for IndicTrans2
        self.lang_code_map = {
            "hi": "hin_Deva",
            "bn": "ben_Beng", 
            "gu": "guj_Gujr",
            "kn": "kan_Knda",
            "ml": "mal_Mlym",
            "mr": "mar_Deva",
            "or": "ory_Orya",
            "pa": "pan_Guru",
            "ta": "tam_Taml",
            "te": "tel_Telu",
            "ur": "urd_Arab",
            "as": "asm_Beng",
            "ne": "nep_Deva",
            "sa": "san_Deva",
            "en": "eng_Latn"
        }
        
        # Reverse mapping for response
        self.reverse_lang_map = {v: k for k, v in self.lang_code_map.items()}
    
    async def load_models(self):
        """Load IndicTrans2 model and language detector based on MODEL_TYPE"""
        if self.model_loaded:
            return
            
        logger.info(f"Starting model loading process (Mode: {MODEL_TYPE}, Device: {self.device})...")
        
        if MODEL_TYPE == "indictrans2":
            try:
                await self._load_language_detector()
                await self._load_translation_model()
                self.model_loaded = True
                logger.info("✅ Real IndicTrans2 models loaded successfully!")
            except Exception as e:
                logger.error(f"❌ Failed to load real models: {str(e)}")
                logger.warning("Falling back to mock implementation.")
                self._use_mock_implementation()
        else:
            self._use_mock_implementation()
            
    def _use_mock_implementation(self):
        """Sets up the service to use mock implementations."""
        logger.info("Using mock implementation for development.")
        self.language_detector = "mock"
        self.model = "mock"
        self.tokenizer = "mock"
        self.model_loaded = True

    async def _download_fasttext_model(self):
        """Downloads the FastText model if it doesn't exist."""
        if not os.path.exists(FASTTEXT_MODEL_PATH):
            logger.info(f"Downloading FastText language detection model from {FASTTEXT_MODEL_URL}...")
            try:
                response = requests.get(FASTTEXT_MODEL_URL, stream=True)
                response.raise_for_status()
                with open(FASTTEXT_MODEL_PATH, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info(f"✅ FastText model downloaded to {FASTTEXT_MODEL_PATH}")
            except Exception as e:
                logger.error(f"❌ Failed to download FastText model: {e}")
                raise
    
    async def _load_language_detector(self):
        """Load FastText language detection model"""
        if not FASTTEXT_AVAILABLE:
            logger.warning("FastText not available, falling back to rule-based detection")
            self.language_detector = "rule_based"
            return
            
        await self._download_fasttext_model()
        try:
            logger.info("Loading FastText language detection model...")
            self.language_detector = fasttext.load_model(FASTTEXT_MODEL_PATH)
            logger.info("✅ FastText model loaded.")
        except Exception as e:
            logger.error(f"❌ Failed to load FastText model: {str(e)}")
            logger.warning("Falling back to rule-based detection")
            self.language_detector = "rule_based"

    async def _load_translation_model(self):
        """Load IndicTrans2 translation model"""
        try:
            logger.info(f"Loading translation model: {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, trust_remote_code=True)
            self.model.to(self.device)
            self.model.eval()
            logger.info("✅ Translation model loaded.")
        except Exception as e:
            logger.error(f"❌ Failed to load translation model: {str(e)}")
            raise
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of input text
        """
        await self.load_models()

        if MODEL_TYPE == "mock" or not FASTTEXT_AVAILABLE or self.language_detector == "rule_based":
            detected_lang = self._rule_based_language_detection(text)
            return {
                "language": detected_lang,
                "confidence": 0.85,
                "language_name": SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            }

        try:
            predictions = self.language_detector.predict(text.replace("\n", " "), k=1)
            lang_code = predictions[0][0].replace('__label__', '')
            confidence = predictions[1][0]
            return {
                "language": lang_code,
                "confidence": confidence,
                "language_name": SUPPORTED_LANGUAGES.get(lang_code, lang_code)
            }
        except Exception as e:
            logger.error(f"Language detection error: {str(e)}")
            # Fallback to rule-based on error
            detected_lang = self._rule_based_language_detection(text)
            return {
                "language": detected_lang,
                "confidence": 0.5,
                "language_name": SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            }
    
    def _rule_based_language_detection(self, text: str) -> str:
        """Simple rule-based language detection for development or fallback"""
        # (Existing rule-based logic remains unchanged)
        # ...
        # Check for Devanagari script (Hindi, Marathi, Sanskrit, Nepali)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return "hi"  # Default to Hindi for Devanagari
        
        # Check for Bengali script
        if any('\u0980' <= char <= '\u09FF' for char in text):
            return "bn"
        
        # Check for Tamil script
        if any('\u0B80' <= char <= '\u0BFF' for char in text):
            return "ta"
        
        # Check for Telugu script
        if any('\u0C00' <= char <= '\u0C7F' for char in text):
            return "te"
        
        # Check for Kannada script
        if any('\u0C80' <= char <= '\u0CFF' for char in text):
            return "kn"
        
        # Check for Malayalam script
        if any('\u0D00' <= char <= '\u0D7F' for char in text):
            return "ml"
        
        # Check for Gujarati script
        if any('\u0A80' <= char <= '\u0AFF' for char in text):
            return "gu"
        
        # Check for Punjabi script
        if any('\u0A00' <= char <= '\u0A7F' for char in text):
            return "pa"
        
        # Check for Odia script
        if any('\u0B00' <= char <= '\u0B7F' for char in text):
            return "or"
        
        # Check for Arabic script (Urdu)
        if any('\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' for char in text):
            return "ur"
        
        # Default to English for Latin script
        return "en"
    
    async def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text from source to target language
        """
        await self.load_models()

        if MODEL_TYPE == "mock":
            translated_text = self._mock_translate(text, source_lang, target_lang)
            return {
                "translated_text": translated_text,
                "confidence": 0.90,
                "model_used": "mock_indictrans2"
            }

        try:
            translated_text = self._indictrans2_translate(text, source_lang, target_lang)
            return {
                "translated_text": translated_text,
                "confidence": 0.95, # Placeholder, real confidence is harder
                "model_used": self.model_name
            }
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                "translated_text": f"[Translation Error: {text}]",
                "confidence": 0.0,
                "model_used": "error_fallback"
            }
    
    def _mock_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Mock translation for development"""
        # (Existing mock logic remains unchanged)
        # ...
        # Simple mock translations for demonstration
        mock_translations = {
            ("hi", "en"): {
                "यह एक अच्छी किताब है": "This is a good book",
                "मुझे यह पसंद है": "I like this",
                "कितना पैसा लगेगा": "How much money will it cost",
                "शुद्ध कपास की साड़ी": "Pure cotton saree",
                "यह एक सुंदर पारंपरिक साड़ी है": "This is a beautiful traditional saree"
            },
            ("en", "hi"): {
                "This is a good book": "यह एक अच्छी किताब है",
                "I like this": "मुझे यह पसंद है",
                "Pure cotton saree": "शुद्ध कपास की साड़ी"
            },
            ("ta", "en"): {
                "இது ஒரு நல்ல புத்தகம்": "This is a good book",
                "எனக்கு இது பிடிக்கும்": "I like this"
            }
        }
        
        translation_dict = mock_translations.get((source_lang, target_lang), {})
        
        # Return mock translation if available, otherwise return a placeholder
        if text in translation_dict:
            return translation_dict[text]
        else:
            return f"[Mock Translation: {text} ({source_lang} -> {target_lang})]"

    def _indictrans2_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Actual IndicTrans2 translation.
        """
        source_code = self.lang_code_map.get(source_lang)
        target_code = self.lang_code_map.get(target_lang)

        if not source_code or not target_code:
            raise ValueError("Unsupported language code provided.")

        # This part requires the IndicTrans2 library's processor
        # For now, we'll simulate the pipeline
        # from IndicTrans2.inference.inference_engine import Model
        # ip = Model(self.model, self.tokenizer, self.device)
        # translated_text = ip.translate_paragraph(text, source_code, target_code)
        
        # Simplified pipeline for direct transformers usage
        inputs = self.tokenizer(text, src_lang=source_code, return_tensors="pt").to(self.device)
        generated_tokens = self.model.generate(**inputs, tgt_lang=target_code, num_return_sequences=1, num_beams=5)
        translated_text = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return translated_text
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        # (Existing logic remains unchanged)
        # ...
        return [
            {"code": code, "name": name}
            for code, name in SUPPORTED_LANGUAGES.items()
            if code in self.lang_code_map
        ]
    
    async def batch_translate(self, texts: List[str], source_lang: str, target_lang: str) -> List[Dict[str, Any]]:
        """
        Translate multiple texts in batch
        """
        # (Existing logic remains unchanged)
        # ...
        results = []
        
        for text in texts:
            result = await self.translate(text, source_lang, target_lang)
            results.append({
                "original_text": text,
                **result
            })
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "translation_model": self.model_name if MODEL_TYPE == 'indictrans2' else 'mock_model',
            "language_detector": "FastText" if MODEL_TYPE == 'indictrans2' else 'rule_based',
            "device": self.device,
            "model_loaded": self.model_loaded,
            "mode": MODEL_TYPE,
            "supported_languages_count": len(self.get_supported_languages()),
        }

