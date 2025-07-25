"""
Translation service using IndicTrans2 by AI4Bharat
Handles language detection and translation between Indian languages
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
import torch
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

# Load environment variables early
load_dotenv()

logger = logging.getLogger(__name__)

# --- Model Configuration ---
FASTTEXT_MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
FASTTEXT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "lid.176.bin")


class TranslationService:
    """Service for handling language detection and translation using IndicTrans2"""
    
    def __init__(self):
        self.en_indic_model = None
        self.en_indic_tokenizer = None
        self.indic_en_model = None
        self.indic_en_tokenizer = None
        self.language_detector = None
        self.device = "cuda" if torch.cuda.is_available() and os.getenv("DEVICE", "cuda") == "cuda" else "cpu"
        self.model_dir = os.getenv("MODEL_PATH", "models/indictrans2")
        self.model_loaded = False
        self.model_type = os.getenv("MODEL_TYPE", "mock")  # Read here instead
        
        # Try to import transformers when needed
        self.transformers_available = False
        try:
            import transformers
            self.transformers_available = True
        except ImportError:
            logger.warning("Transformers not available, will use mock mode")
        
        # Language code mappings for IndicTrans2 (ISO to Flores codes)
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
        
        # Language name to code mapping for API requests
        self.lang_name_to_code = {
            "English": "en",
            "Hindi": "hi",
            "Bengali": "bn",
            "Gujarati": "gu",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Marathi": "mr",
            "Oriya": "or",
            "Punjabi": "pa",
            "Tamil": "ta",
            "Telugu": "te",
            "Urdu": "ur",
            "Assamese": "as",
            "Nepali": "ne",
            "Sanskrit": "sa"
        }
        
        # Reverse mapping for response
        self.reverse_lang_map = {v: k for k, v in self.lang_code_map.items()}
    
    async def load_models(self):
        """Load IndicTrans2 model and language detector based on MODEL_TYPE"""
        if self.model_loaded:
            return
            
        logger.info(f"Starting model loading process (Mode: {self.model_type}, Device: {self.device})...")
        
        if self.model_type == "indictrans2" and self.transformers_available:
            try:
                await self._load_language_detector()
                await self._load_indictrans2_model()
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
        self.en_indic_model = "mock"
        self.en_indic_tokenizer = "mock"
        self.indic_en_model = "mock"
        self.indic_en_tokenizer = "mock"
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

    async def _load_indictrans2_model(self):
        """Load IndicTrans2 translation models using Hugging Face transformers"""
        try:
            # Import transformers here to avoid import-time errors
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            logger.info(f"Loading IndicTrans2 models from: {self.model_dir}...")
            
            # Get the correct model paths (relative to the project root, not backend folder)
            import os
            # Get the project root (one level up from backend)
            current_dir = os.path.dirname(__file__)  # backend directory
            project_root = os.path.dirname(current_dir)  # project root
            
            en_indic_path = os.path.join(project_root, "models", "indictrans2", "indictrans2-en-indic-1B")
            indic_en_path = os.path.join(project_root, "models", "indictrans2", "indictrans2-indic-en-1B")
            
            logger.info(f"Loading EN→Indic model from {en_indic_path}...")
            self.en_indic_tokenizer = AutoTokenizer.from_pretrained(en_indic_path, trust_remote_code=True)
            self.en_indic_model = AutoModelForSeq2SeqLM.from_pretrained(en_indic_path, trust_remote_code=True)
            self.en_indic_model.to(self.device)
            self.en_indic_model.eval()
            
            logger.info(f"Loading Indic→EN model from {indic_en_path}...")
            self.indic_en_tokenizer = AutoTokenizer.from_pretrained(indic_en_path, trust_remote_code=True)
            self.indic_en_model = AutoModelForSeq2SeqLM.from_pretrained(indic_en_path, trust_remote_code=True)
            self.indic_en_model.to(self.device)
            self.indic_en_model.eval()
            
            logger.info("✅ IndicTrans2 models loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load IndicTrans2 models: {str(e)}")
            logger.error("Make sure you have:")
            logger.error("1. Downloaded the IndicTrans2 model files")
            logger.error("2. Set the correct MODEL_PATH in .env")
            logger.error("3. Installed all required dependencies")
            raise
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of input text
        """
        await self.load_models()

        if self.model_type == "mock" or not FASTTEXT_AVAILABLE or self.language_detector == "rule_based":
            detected_lang = self._rule_based_language_detection(text)
            return {
                "language": detected_lang,
                "confidence": 0.85,
                "language_name": SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            }

        try:
            # Use FastText for language detection
            predictions = self.language_detector.predict(text.replace('\n', ' '), k=1)
            detected_lang_code = predictions[0][0].replace('__label__', '')
            confidence = float(predictions[1][0])
            
            # Map to our supported languages
            lang_mapping = {
                'hi': 'hi', 'bn': 'bn', 'gu': 'gu', 'kn': 'kn', 'ml': 'ml',
                'mr': 'mr', 'or': 'or', 'pa': 'pa', 'ta': 'ta', 'te': 'te',
                'ur': 'ur', 'as': 'as', 'ne': 'ne', 'sa': 'sa', 'en': 'en'
            }
            
            detected_lang = lang_mapping.get(detected_lang_code, 'en')
            
            return {
                "language": detected_lang,
                "confidence": confidence,
                "language_name": SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            }
            
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            # Fallback to rule-based detection
            detected_lang = self._rule_based_language_detection(text)
            return {
                "language": detected_lang,
                "confidence": 0.50,
                "language_name": SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            }
    
    def _rule_based_language_detection(self, text: str) -> str:
        """Simple rule-based language detection as fallback"""
        text_lower = text.lower()
        
        # Check for English indicators
        english_words = ['the', 'and', 'is', 'in', 'to', 'of', 'for', 'with', 'on', 'at']
        if any(word in text_lower for word in english_words):
            return 'en'
        
        # Check for Hindi indicators (Devanagari script)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return 'hi'
        
        # Check for Bengali indicators
        if any('\u0980' <= char <= '\u09FF' for char in text):
            return 'bn'
        
        # Check for Tamil indicators
        if any('\u0B80' <= char <= '\u0BFF' for char in text):
            return 'ta'
        
        # Check for Telugu indicators
        if any('\u0C00' <= char <= '\u0C7F' for char in text):
            return 'te'
        
        # Default to English
        return 'en'
    
    async def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text from source language to target language using IndicTrans2
        """
        await self.load_models()
        
        if self.model_type == "mock" or self.en_indic_model == "mock":
            return self._mock_translate(text, source_lang, target_lang)
        
        try:
            # Convert language names to codes if needed
            src_lang_code = self.lang_name_to_code.get(source_lang, source_lang)
            tgt_lang_code = self.lang_name_to_code.get(target_lang, target_lang)
            
            logger.info(f"Converting {source_lang} -> {src_lang_code}, {target_lang} -> {tgt_lang_code}")
            
            # Map language codes to IndicTrans2 format
            src_code = self.lang_code_map.get(src_lang_code, src_lang_code)
            tgt_code = self.lang_code_map.get(tgt_lang_code, tgt_lang_code)
            
            logger.info(f"Using IndicTrans2 codes: {src_code} -> {tgt_code}")
            
            # Choose the right model and tokenizer based on direction
            if src_lang_code == "en" and tgt_lang_code != "en":
                # English to Indic
                model = self.en_indic_model
                tokenizer = self.en_indic_tokenizer
                input_text = f"{src_code} {tgt_code} {text}"
            elif src_lang_code != "en" and tgt_lang_code == "en":
                # Indic to English
                model = self.indic_en_model
                tokenizer = self.indic_en_tokenizer
                input_text = f"{src_code} {tgt_code} {text}"
            else:
                # For Indic to Indic, use English as pivot (not ideal but works)
                if src_lang_code != "en":
                    # First translate to English
                    intermediate_result = await self.translate(text, src_lang_code, "en")
                    intermediate_text = intermediate_result["translated_text"]
                    # Then translate from English to target
                    return await self.translate(intermediate_text, "en", tgt_lang_code)
                else:
                    # Same language, return as is
                    return {
                        "translated_text": text,
                        "source_language": source_lang,
                        "target_language": target_lang,
                        "model": "IndicTrans2 (No translation needed)",
                        "confidence": 1.0
                    }
            
            # Tokenize and translate
            inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=512, num_beams=5, do_sample=False)
            
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "model": "IndicTrans2",
                "confidence": 0.92
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Fallback to mock translation
            return self._mock_translate(text, source_lang, target_lang)
    
    def _mock_translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Mock translation for development and fallback"""
        mock_translations = {
            ("en", "hi"): "नमस्ते, यह एक परीक्षण अनुवाद है।",
            ("hi", "en"): "Hello, this is a test translation.",
            ("en", "bn"): "হ্যালো, এটি একটি পরীক্ষা অনুবাদ।",
            ("bn", "en"): "Hello, this is a test translation.",
            ("en", "ta"): "வணக்கம், இது ஒரு சோதனை மொழிபெயர்ப்பு.",
            ("ta", "en"): "Hello, this is a test translation."
        }
        
        translated_text = mock_translations.get(
            (source_lang, target_lang), 
            f"[MOCK] Translated from {source_lang} to {target_lang}: {text}"
        )
        
        return {
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "model": "Mock (Development)",
            "confidence": 0.75
        }

    async def batch_translate(self, texts: List[str], source_lang: str, target_lang: str) -> List[Dict[str, Any]]:
        """
        Translate multiple texts in batch for efficiency
        """
        await self.load_models()
        
        if self.model_type == "mock" or self.en_indic_model == "mock":
            return [self._mock_translate(text, source_lang, target_lang) for text in texts]
        
        try:
            results = []
            for text in texts:
                result = await self.translate(text, source_lang, target_lang)
                result["original_text"] = text
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Batch translation failed: {str(e)}")
            # Fallback to individual mock translations
            return [self._mock_translate(text, source_lang, target_lang) for text in texts]

    def get_supported_languages(self) -> Dict[str, str]:
        """Return supported languages"""
        return SUPPORTED_LANGUAGES

    def is_translation_supported(self, source_lang: str, target_lang: str) -> bool:
        """Check if translation between two languages is supported"""
        return source_lang in SUPPORTED_LANGUAGES and target_lang in SUPPORTED_LANGUAGES

# Global service instance
translation_service = TranslationService()

async def get_translation_service() -> TranslationService:
    """Dependency injection for FastAPI"""
    return translation_service
