"""
Lightweight backend simulation for Streamlit Cloud deployment
This provides realistic mock responses for demonstration purposes
"""

import random
import time
from typing import Dict, List
import pandas as pd
from datetime import datetime

class CloudTranslationService:
    """Mock translation service for cloud deployment"""
    
    def __init__(self):
        self.languages = {
            "en": "English", "hi": "Hindi", "bn": "Bengali", 
            "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
            "mr": "Marathi", "or": "Odia", "pa": "Punjabi",
            "ta": "Tamil", "te": "Telugu", "ur": "Urdu",
            "as": "Assamese", "ne": "Nepali", "sa": "Sanskrit"
        }
        
        # High-quality sample translations for realistic demo
        self.sample_translations = {
            # English to Hindi
            ("hello", "en", "hi"): "नमस्ते",
            ("smartphone", "en", "hi"): "स्मार्टफोन",
            ("book", "en", "hi"): "किताब",
            ("computer", "en", "hi"): "कंप्यूटर",
            ("beautiful", "en", "hi"): "सुंदर",
            ("premium smartphone with 128gb storage", "en", "hi"): "128GB स्टोरेज के साथ प्रीमियम स्मार्टफोन",
            ("wireless bluetooth headphones", "en", "hi"): "वायरलेस ब्लूटूथ हेडफोन्स",
            ("cotton t-shirt for men", "en", "hi"): "पुरुषों के लिए कॉटन टी-शर्ट",
            ("electronics", "en", "hi"): "इलेक्ट्रॉनिक्स",
            ("clothing", "en", "hi"): "वस्त्र",
            
            # English to Tamil
            ("hello", "en", "ta"): "வணக்கம்",
            ("smartphone", "en", "ta"): "ஸ்மார்ட்ஃபோன்",
            ("book", "en", "ta"): "புத்தகம்",
            ("computer", "en", "ta"): "கணினி",
            ("beautiful", "en", "ta"): "அழகான",
            ("premium smartphone with 128gb storage", "en", "ta"): "128GB சேமிப்பகத்துடன் பிரீமியம் ஸ்மார்ட்ஃபோன்",
            ("wireless bluetooth headphones", "en", "ta"): "வயர்லெஸ் புளூடூத் ஹெட்ஃபோன்கள்",
            ("cotton t-shirt for men", "en", "ta"): "ஆண்களுக்கான பருத்தி டி-ஷர்ட்",
            ("electronics", "en", "ta"): "மின்னணுவியல்",
            ("clothing", "en", "ta"): "உடைகள்",
            
            # English to Telugu
            ("hello", "en", "te"): "నమస్కారం",
            ("smartphone", "en", "te"): "స్మార్ట్‌ఫోన్",
            ("book", "en", "te"): "పుస్తకం",
            ("computer", "en", "te"): "కంప్యూటర్",
            ("beautiful", "en", "te"): "అందమైన",
            ("premium smartphone with 128gb storage", "en", "te"): "128GB నిల్వతో ప్రీమియం స్మార్ట్‌ఫోన్",
            ("wireless bluetooth headphones", "en", "te"): "వైర్‌లెస్ బ్లూటూత్ హెడ్‌ఫోన్‌లు",
            ("cotton t-shirt for men", "en", "te"): "పురుషుల కోసం కాటన్ టీ-షర్ట్",
            ("electronics", "en", "te"): "ఎలక్ట్రానిక్స్",
            ("clothing", "en", "te"): "దుస్తులు",
            
            # English to Bengali
            ("hello", "en", "bn"): "নমস্কার",
            ("smartphone", "en", "bn"): "স্মার্টফোন",
            ("book", "en", "bn"): "বই",
            ("premium smartphone with 128gb storage", "en", "bn"): "১২৮জিবি স্টোরেজ সহ প্রিমিয়াম স্মার্টফোন",
            ("electronics", "en", "bn"): "ইলেকট্রনিক্স",
            
            # English to Gujarati
            ("hello", "en", "gu"): "નમસ્તે",
            ("smartphone", "en", "gu"): "સ્માર્ટફોન",
            ("premium smartphone with 128gb storage", "en", "gu"): "128GB સ્ટોરેજ સાથે પ્રીમિયમ સ્માર્ટફોન",
            ("electronics", "en", "gu"): "ઇલેક્ટ્રોનિક્સ",
        }
        
        # Mock translation history
        self.history = []
        self._generate_sample_history()
    
    def _generate_sample_history(self):
        """Generate realistic sample history"""
        sample_data = [
            ("Premium Smartphone with 128GB storage", "128GB स्टोरेज के साथ प्रीमियम स्मार्टफोन", "en", "hi", 0.94),
            ("Wireless Bluetooth Headphones", "वायरलेस ब्लूटूथ हेडफोन्स", "en", "hi", 0.91),
            ("Cotton T-Shirt for Men", "पुरुषों के लिए कॉटन टी-शर्ट", "en", "hi", 0.89),
            ("Premium Smartphone with 128GB storage", "128GB சேமிப்பகத்துடன் பிரீமியம் ஸ்மார்ட்ஃபோன்", "en", "ta", 0.92),
            ("Wireless Bluetooth Headphones", "వైర్‌లెస్ బ্లূটూత్ హెడ్‌ఫోన్‌లు", "en", "te", 0.90),
            ("Smart Watch with Fitness Tracker", "ফিটনেস ট্র্যাকার সহ স্মার্ট ঘড়ি", "en", "bn", 0.88),
            ("Leather Wallet for Women", "મહિલાઓ માટે ચામડાનું વૅલેટ", "en", "gu", 0.87),
            ("Gaming Laptop 16GB RAM", "गेमिंग लैपटॉप 16GB RAM", "en", "hi", 0.93),
            ("Organic Green Tea", "জৈব সবুজ চা", "en", "bn", 0.90),
            ("Traditional Silk Saree", "பாரம்பரிய பட்டு சேலை", "en", "ta", 0.95),
        ]
        
        for i, (orig, trans, src, tgt, conf) in enumerate(sample_data):
            self.history.append({
                "id": i + 1,
                "original_text": orig,
                "translated_text": trans,
                "source_language": src,
                "target_language": tgt,
                "model_confidence": conf,
                "created_at": "2025-01-25T10:30:00",
                "corrected_text": None
            })
    
    def detect_language(self, text: str) -> Dict:
        """Mock language detection with basic heuristics"""
        text_lower = text.lower()
        
        # Hindi detection
        if any(char in text for char in "अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह"):
            return {"language": "hi", "confidence": 0.95, "language_name": "Hindi"}
        
        # Tamil detection
        elif any(char in text for char in "அஆஇஈஉஊஎஏஐஒஓஔகஙசஞடணதநபமயரலவழளறன"):
            return {"language": "ta", "confidence": 0.94, "language_name": "Tamil"}
        
        # Telugu detection
        elif any(char in text for char in "అఆఇఈఉఊఎఏఐఒఓఔకఖగఘచఛజఝటఠడఢణతథదధనపఫబభమయరలవశషసహ"):
            return {"language": "te", "confidence": 0.93, "language_name": "Telugu"}
        
        # Bengali detection
        elif any(char in text for char in "অআইঈউঊএঐওঔকখগঘচছজঝটঠডঢণতথদধনপফবভমযরলশষসহ"):
            return {"language": "bn", "confidence": 0.92, "language_name": "Bengali"}
        
        # Gujarati detection
        elif any(char in text for char in "અઆઇઈઉઊએઐઓઔકખગઘચછજઝટઠડઢણતથદધનપફબભમયરલવશષસહ"):
            return {"language": "gu", "confidence": 0.91, "language_name": "Gujarati"}
        
        # Default to English
        else:
            return {"language": "en", "confidence": 0.98, "language_name": "English"}
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Mock translation with realistic responses"""
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        # Normalize input for lookup
        text_normalized = text.lower().strip()
        key = (text_normalized, source_lang, target_lang)
        
        # Check for exact matches first
        if key in self.sample_translations:
            translated = self.sample_translations[key]
            confidence = round(random.uniform(0.88, 0.96), 2)
        else:
            # Generate context-aware translations based on keywords
            translated = self._generate_contextual_translation(text, source_lang, target_lang)
            confidence = round(random.uniform(0.82, 0.94), 2)
        
        # Add to history
        translation_id = len(self.history) + 1
        self.history.append({
            "id": translation_id,
            "original_text": text,
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": target_lang,
            "model_confidence": confidence,
            "created_at": datetime.now().isoformat(),
            "corrected_text": None
        })
        
        return {
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": target_lang,
            "confidence": confidence,
            "translation_id": translation_id
        }
    
    def _generate_contextual_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate contextual translations based on keywords"""
        text_lower = text.lower()
        
        # E-commerce specific translations
        if target_lang == "hi":
            if "smartphone" in text_lower or "phone" in text_lower:
                return f"स्मार्टफोन - {text}"
            elif "laptop" in text_lower or "computer" in text_lower:
                return f"लैपटॉप - {text}"
            elif "shirt" in text_lower or "clothing" in text_lower:
                return f"शर्ट/वस्त्र - {text}"
            elif "book" in text_lower:
                return f"किताब - {text}"
            elif "headphone" in text_lower or "earphone" in text_lower:
                return f"हेडफोन - {text}"
            else:
                return f"[हिंदी अनुवाद] {text}"
                
        elif target_lang == "ta":
            if "smartphone" in text_lower or "phone" in text_lower:
                return f"ஸ்மார்ட்ஃபோன் - {text}"
            elif "laptop" in text_lower or "computer" in text_lower:
                return f"லேப்டாப் - {text}"
            elif "shirt" in text_lower or "clothing" in text_lower:
                return f"சட்டை/உடைகள் - {text}"
            elif "book" in text_lower:
                return f"புத்தகம் - {text}"
            else:
                return f"[தமிழ் மொழிபெயர்ப்பு] {text}"
                
        elif target_lang == "te":
            if "smartphone" in text_lower or "phone" in text_lower:
                return f"స్మార్ట్‌ఫోన్ - {text}"
            elif "laptop" in text_lower or "computer" in text_lower:
                return f"ల్యాప్‌టాప్ - {text}"
            elif "shirt" in text_lower or "clothing" in text_lower:
                return f"చొక్కా/దుస్తులు - {text}"
            elif "book" in text_lower:
                return f"పుస్తకం - {text}"
            else:
                return f"[తెలుగు అనువాదం] {text}"
                
        elif target_lang == "bn":
            if "smartphone" in text_lower or "phone" in text_lower:
                return f"স্মার্টফোন - {text}"
            elif "laptop" in text_lower or "computer" in text_lower:
                return f"ল্যাপটপ - {text}"
            elif "book" in text_lower:
                return f"বই - {text}"
            else:
                return f"[বাংলা অনুবাদ] {text}"
                
        elif target_lang == "gu":
            if "smartphone" in text_lower or "phone" in text_lower:
                return f"સ્માર્ટફોન - {text}"
            elif "laptop" in text_lower or "computer" in text_lower:
                return f"લેપટોપ - {text}"
            else:
                return f"[ગુજરાતી અનુવાદ] {text}"
        
        # Default fallback
        lang_name = self.languages.get(target_lang, target_lang)
        return f"[{lang_name} Translation] {text}"
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Get translation history"""
        return self.history[-limit:]
    
    def submit_correction(self, translation_id: int, corrected_text: str, feedback: str = "") -> Dict:
        """Submit correction"""
        for item in self.history:
            if item["id"] == translation_id:
                item["corrected_text"] = corrected_text
                break
        
        return {
            "correction_id": random.randint(1000, 9999),
            "message": "Correction submitted successfully",
            "status": "success"
        }
    
    def get_supported_languages(self) -> Dict:
        """Get supported languages"""
        return {
            "languages": self.languages,
            "total_count": len(self.languages)
        }

# Global instance
cloud_service = CloudTranslationService()
