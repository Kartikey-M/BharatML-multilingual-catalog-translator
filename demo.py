"""
Demo script for Multi-Lingual Product Catalog Translator
Shows sample translations and functionality
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from translation_service import TranslationService
from database import DatabaseManager

async def run_demo():
    """Run demonstration of the translation system"""
    
    print("🌐 Multi-Lingual Product Catalog Translator Demo")
    print("=" * 50)
    
    # Initialize services
    print("🔧 Initializing translation service...")
    translation_service = TranslationService()
    await translation_service.load_models()
    
    print("🗄️ Initializing database...")
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Sample product data
    sample_products = [
        {
            "title": "शुद्ध कपास की साड़ी",
            "description": "यह एक सुंदर पारंपरिक साड़ी है जो शुद्ध कपास से बनी है। विशेष अवसरों के लिए आदर्श।",
            "category": "वस्त्र",
            "source_lang": "hi"
        },
        {
            "title": "Pure Cotton Saree", 
            "description": "This is a beautiful traditional saree made from pure cotton. Perfect for special occasions.",
            "category": "Clothing",
            "source_lang": "en"
        },
        {
            "title": "மென்மையான பட்டுப் புடவை",
            "description": "இது மிகவும் அழகான பட்டுப் புடவை. திருமண நிகழ்ச்சிகளுக்கு ஏற்றது.",
            "category": "ஆடைகள்",
            "source_lang": "ta"
        }
    ]
    
    target_languages = ["en", "hi", "ta", "te", "bn"]
    
    print("\n📝 Sample Product Translations")
    print("-" * 30)
    
    for i, product in enumerate(sample_products, 1):
        print(f"\n🛍️ Product {i}:")
        print(f"Source Language: {product['source_lang']}")
        print(f"Title: {product['title']}")
        print(f"Description: {product['description'][:60]}...")
        
        # Detect language
        detection_result = await translation_service.detect_language(product['title'])
        print(f"🔍 Detected Language: {detection_result['language']} (confidence: {detection_result['confidence']:.2%})")
        
        # Translate to different languages
        print("\n🌐 Translations:")
        for target_lang in target_languages:
            if target_lang == product['source_lang']:
                continue  # Skip same language
            
            # Translate title
            title_result = await translation_service.translate(
                product['title'],
                product['source_lang'],
                target_lang
            )
            
            # Store in database
            translation_id = db_manager.store_translation(
                original_text=product['title'],
                translated_text=title_result['translated_text'],
                source_language=product['source_lang'],
                target_language=target_lang,
                model_confidence=title_result['confidence']
            )
            
            print(f"  {target_lang}: {title_result['translated_text']} (ID: {translation_id})")
        
        print("-" * 50)
    
    # Show database statistics
    print("\n📊 Database Statistics:")
    stats = db_manager.get_statistics()
    print(f"Total Translations: {stats['total_translations']}")
    print(f"Total Corrections: {stats['total_corrections']}")
    print(f"Language Pairs:")
    for pair in stats['language_pairs'][:5]:  # Show top 5
        print(f"  {pair['source']} → {pair['target']}: {pair['count']} translations")
    
    # Show supported languages
    print("\n🌍 Supported Languages:")
    languages = translation_service.get_supported_languages()
    for lang in languages:
        print(f"  {lang['code']}: {lang['name']}")
    
    print("\n✅ Demo completed successfully!")
    print("\n🚀 To start the full application:")
    print("1. Backend: cd backend && python main.py")
    print("2. Frontend: cd frontend && streamlit run app.py")
    print("3. Open browser: http://localhost:8501")

if __name__ == "__main__":
    asyncio.run(run_demo())
