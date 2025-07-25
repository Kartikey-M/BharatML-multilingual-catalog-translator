#!/usr/bin/env python3
"""
Test script for IndicTrans2 integration
This script tests both mock and real mode functionality
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from translation_service import TranslationService

async def test_translation_service():
    """Test the translation service"""
    print("🧪 Testing IndicTrans2 Integration")
    print("=" * 50)
    
    # Create service instance
    service = TranslationService()
    
    # Test language detection
    print("\n1. Testing Language Detection...")
    test_texts = [
        "Hello, how are you?",
        "नमस्ते, आप कैसे हैं?",
        "হ্যালো, আপনি কেমন আছেন?",
        "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?"
    ]
    
    for text in test_texts:
        result = await service.detect_language(text)
        print(f"Text: {text}")
        print(f"Detected: {result['language']} ({result['language_name']}) - Confidence: {result['confidence']:.2f}")
        print()
    
    # Test translation
    print("2. Testing Translation...")
    translations = [
        ("Hello, welcome to our store!", "en", "hi"),
        ("This is a quality product.", "en", "bn"),
        ("Thank you for your purchase.", "en", "ta"),
        ("नमस्ते, हमारे स्टोर में आपका स्वागत है!", "hi", "en")
    ]
    
    for text, src, tgt in translations:
        result = await service.translate(text, src, tgt)
        print(f"Source ({src}): {text}")
        print(f"Target ({tgt}): {result['translated_text']}")
        print(f"Model: {result['model']} - Confidence: {result['confidence']:.2f}")
        print()
    
    # Test batch translation
    print("3. Testing Batch Translation...")
    batch_texts = [
        "Welcome to our online store",
        "Browse our products",
        "Add to cart",
        "Checkout now"
    ]
    
    batch_results = await service.batch_translate(batch_texts, "en", "hi")
    for i, result in enumerate(batch_results):
        print(f"Original: {batch_texts[i]}")
        print(f"Translated: {result['translated_text']}")
        print()
    
    print("✅ All tests completed!")
    print(f"Current mode: {os.getenv('MODEL_TYPE', 'mock')}")
    if os.getenv('MODEL_TYPE') == 'mock':
        print("💡 To test real mode:")
        print("   1. Download IndicTrans2 models to models/indictrans2/")
        print("   2. Set MODEL_TYPE=indictrans2 in .env")
        print("   3. Run this test again")

if __name__ == "__main__":
    asyncio.run(test_translation_service())
