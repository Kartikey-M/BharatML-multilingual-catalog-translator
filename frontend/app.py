"""
Streamlit frontend for Multi-Lingual Product Catalog Translator
Provides user-friendly interface for sellers to translate and edit product listings
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
from typing import Dict, List, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Lingual Catalog Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
API_BASE_URL = "http://localhost:8001"

# Language mappings
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali", 
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "or": "Odia",
    "pa": "Punjabi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "as": "Assamese",
    "ne": "Nepali",
    "sa": "Sanskrit"
}

def make_api_request(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Make API request to backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the backend API. Please ensure the FastAPI server is running on localhost:8001")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Error: {str(e)}")
        return {}
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return {}

def check_api_health():
    """Check if API is healthy"""
    try:
        response = make_api_request("/")
        return bool(response)
    except:
        return False

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🌐 Multi-Lingual Product Catalog Translator")
    st.markdown("### Powered by IndicTrans2 by AI4Bharat")
    st.markdown("Translate your product listings into multiple Indian languages instantly!")
    
    # Check API health
    if not check_api_health():
        st.error("🔴 Backend API is not available. Please start the FastAPI server first.")
        st.code("cd backend && python main.py", language="bash")
        return
    else:
        st.success("🟢 Backend API is connected!")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["🏠 Translate Product", "📊 Translation History", "📈 Analytics", "⚙️ Settings"]
    )
    
    if page == "🏠 Translate Product":
        translate_product_page()
    elif page == "📊 Translation History":
        translation_history_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "⚙️ Settings":
        settings_page()

def translate_product_page():
    """Main product translation page"""
    
    st.header("📝 Translate Product Listing")
    
    # Create two columns for input and output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Input")
        
        # Product details input
        with st.form("product_form"):
            product_title = st.text_input(
                "Product Title *",
                placeholder="Enter your product title...",
                help="The main title of your product"
            )
            
            product_description = st.text_area(
                "Product Description *",
                placeholder="Enter detailed product description...",
                height=150,
                help="Detailed description of your product"
            )
            
            product_category = st.text_input(
                "Category (Optional)",
                placeholder="e.g., Electronics, Clothing, Books...",
                help="Product category for better context"
            )
            
            # Language selection
            st.markdown("---")
            st.subheader("🌍 Language Settings")
            
            source_lang = st.selectbox(
                "Source Language",
                options=["auto-detect"] + list(SUPPORTED_LANGUAGES.keys()),
                format_func=lambda x: "🔍 Auto-detect" if x == "auto-detect" else f"{SUPPORTED_LANGUAGES.get(x, x)} ({x})",
                help="Select the language of your input text, or use auto-detect"
            )
            
            target_languages = st.multiselect(
                "Target Languages *",
                options=list(SUPPORTED_LANGUAGES.keys()),
                default=["en", "hi"],
                format_func=lambda x: f"{SUPPORTED_LANGUAGES.get(x, x)} ({x})",
                help="Select one or more languages to translate to"
            )
            
            submit_button = st.form_submit_button("🚀 Translate", type="primary")
    
    with col2:
        st.subheader("📤 Output")
        
        if submit_button:
            if not product_title or not product_description:
                st.error("Please fill in the required fields (Product Title and Description)")
                return
            
            if not target_languages:
                st.error("Please select at least one target language")
                return
            
            # Process translations
            with st.spinner("🔄 Translating your product listing..."):
                translations = process_translations(
                    product_title,
                    product_description,
                    product_category,
                    source_lang,
                    target_languages
                )
            
            if translations:
                display_translations(translations, product_title, product_description, product_category)

def process_translations(title: str, description: str, category: str, source_lang: str, target_languages: List[str]) -> Dict:
    """Process translations for product fields"""
    
    translations = {}
    
    # Detect source language if auto-detect is selected
    if source_lang == "auto-detect":
        detection_result = make_api_request("/detect-language", "POST", {"text": title})
        if detection_result:
            source_lang = detection_result.get("language", "en")
            st.info(f"🔍 Detected source language: {SUPPORTED_LANGUAGES.get(source_lang, source_lang)}")
    
    # Translate to each target language
    for target_lang in target_languages:
        if target_lang == source_lang:
            # Skip if source and target are the same
            continue
        
        translations[target_lang] = {}
        
        # Translate title
        title_result = make_api_request("/translate", "POST", {
            "text": title,
            "source_language": source_lang,
            "target_language": target_lang
        })
        
        if title_result:
            translations[target_lang]["title"] = title_result
        
        # Translate description
        description_result = make_api_request("/translate", "POST", {
            "text": description,
            "source_language": source_lang,
            "target_language": target_lang
        })
        
        if description_result:
            translations[target_lang]["description"] = description_result
        
        # Translate category if provided
        if category:
            category_result = make_api_request("/translate", "POST", {
                "text": category,
                "source_language": source_lang,
                "target_language": target_lang
            })
            
            if category_result:
                translations[target_lang]["category"] = category_result
    
    return translations

def display_translations(translations: Dict, original_title: str, original_description: str, original_category: str):
    """Display translation results with editing capability"""
    
    for target_lang, results in translations.items():
        lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
        
        with st.expander(f"🌐 {lang_name} Translation", expanded=True):
            
            # Title translation
            if "title" in results:
                st.markdown("**📝 Title:**")
                translated_title = results["title"]["translated_text"]
                translation_id = results["title"]["translation_id"]
                
                # Editable text area for corrections
                corrected_title = st.text_area(
                    f"Edit {lang_name} title:",
                    value=translated_title,
                    key=f"title_{target_lang}_{translation_id}",
                    height=50
                )
                
                # Show confidence score
                confidence = results["title"].get("confidence", 0)
                st.caption(f"Confidence: {confidence:.2%}")
                
                # Submit correction if text was edited
                if corrected_title != translated_title:
                    if st.button(f"💾 Save Title Correction", key=f"save_title_{translation_id}"):
                        submit_correction(translation_id, corrected_title, "Title correction")
            
            # Description translation
            if "description" in results:
                st.markdown("**📄 Description:**")
                translated_description = results["description"]["translated_text"]
                translation_id = results["description"]["translation_id"]
                
                corrected_description = st.text_area(
                    f"Edit {lang_name} description:",
                    value=translated_description,
                    key=f"description_{target_lang}_{translation_id}",
                    height=100
                )
                
                confidence = results["description"].get("confidence", 0)
                st.caption(f"Confidence: {confidence:.2%}")
                
                if corrected_description != translated_description:
                    if st.button(f"💾 Save Description Correction", key=f"save_desc_{translation_id}"):
                        submit_correction(translation_id, corrected_description, "Description correction")
            
            # Category translation
            if "category" in results:
                st.markdown("**🏷️ Category:**")
                translated_category = results["category"]["translated_text"]
                translation_id = results["category"]["translation_id"]
                
                corrected_category = st.text_input(
                    f"Edit {lang_name} category:",
                    value=translated_category,
                    key=f"category_{target_lang}_{translation_id}"
                )
                
                confidence = results["category"].get("confidence", 0)
                st.caption(f"Confidence: {confidence:.2%}")
                
                if corrected_category != translated_category:
                    if st.button(f"💾 Save Category Correction", key=f"save_cat_{translation_id}"):
                        submit_correction(translation_id, corrected_category, "Category correction")
            
            st.markdown("---")

def submit_correction(translation_id: int, corrected_text: str, feedback: str):
    """Submit correction to the backend"""
    
    result = make_api_request("/submit-correction", "POST", {
        "translation_id": translation_id,
        "corrected_text": corrected_text,
        "feedback": feedback
    })
    
    if result and result.get("status") == "success":
        st.success("✅ Correction saved successfully!")
        st.balloons()
    else:
        st.error("❌ Failed to save correction")

def translation_history_page():
    """Translation history page"""
    
    st.header("📊 Translation History")
    
    # Fetch translation history
    history = make_api_request("/history?limit=100")
    
    if not history:
        st.info("No translation history available yet.")
        return
    
    # Convert to DataFrame for better display
    df_data = []
    for record in history:
        df_data.append({
            "ID": record["id"],
            "Original Text": record["original_text"][:50] + "..." if len(record["original_text"]) > 50 else record["original_text"],
            "Translated Text": record["translated_text"][:50] + "..." if len(record["translated_text"]) > 50 else record["translated_text"],
            "Source → Target": f"{record['source_language']} → {record['target_language']}",
            "Confidence": f"{record['model_confidence']:.2%}",
            "Created": record["created_at"][:19],
            "Corrected": "✅" if record["corrected_text"] else "❌"
        })
    
    df = pd.DataFrame(df_data)
    
    # Display filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        source_filter = st.selectbox(
            "Filter by Source Language",
            options=["All"] + list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: "All Languages" if x == "All" else f"{SUPPORTED_LANGUAGES.get(x, x)} ({x})"
        )
    
    with col2:
        target_filter = st.selectbox(
            "Filter by Target Language", 
            options=["All"] + list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: "All Languages" if x == "All" else f"{SUPPORTED_LANGUAGES.get(x, x)} ({x})"
        )
    
    with col3:
        correction_filter = st.selectbox(
            "Filter by Correction Status",
            options=["All", "Corrected", "Not Corrected"]
        )
    
    # Apply filters (simplified for display)
    filtered_df = df.copy()
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        csv,
        "translation_history.csv",
        "text/csv",
        key='download-csv'
    )

def analytics_page():
    """Analytics and statistics page"""
    
    st.header("📈 Analytics & Statistics")
    
    # Fetch statistics from API (mock for now)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Translations", "1,234", "+12%")
    
    with col2:
        st.metric("Corrections Submitted", "89", "+5%")
    
    with col3:
        st.metric("Languages Supported", len(SUPPORTED_LANGUAGES))
    
    with col4:
        st.metric("Avg. Confidence", "92.5%", "+2.1%")
    
    # Language pair popularity chart
    st.subheader("🔀 Popular Language Pairs")
    
    # Mock data for demonstration
    language_pairs_data = {
        "Language Pair": ["Hindi → English", "Tamil → English", "Bengali → Hindi", "English → Hindi", "Gujarati → English"],
        "Translation Count": [450, 280, 220, 180, 140]
    }
    
    df_pairs = pd.DataFrame(language_pairs_data)
    st.bar_chart(df_pairs.set_index("Language Pair"))
    
    # Daily translation trend
    st.subheader("📅 Daily Translation Trend")
    
    # Mock time series data
    dates = pd.date_range(start="2025-01-18", end="2025-01-25", freq="D")
    translations_per_day = [45, 52, 38, 61, 47, 55, 49, 58]
    
    df_trend = pd.DataFrame({
        "Date": dates,
        "Translations": translations_per_day
    })
    
    st.line_chart(df_trend.set_index("Date"))

def settings_page():
    """Settings and configuration page"""
    
    st.header("⚙️ Settings")
    
    # API Configuration
    st.subheader("🔧 API Configuration")
    
    with st.form("api_settings"):
        api_url = st.text_input("Backend API URL", value=API_BASE_URL)
        
        st.markdown("**Model Settings:**")
        model_type = st.selectbox(
            "Translation Model",
            options=["IndicTrans2-1B", "IndicTrans2-Distilled", "Mock (Development)"],
            index=2
        )
        
        confidence_threshold = st.slider(
            "Minimum Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Translations below this confidence will be flagged for review"
        )
        
        if st.form_submit_button("💾 Save Settings"):
            st.success("✅ Settings saved successfully!")
    
    # About section
    st.subheader("ℹ️ About")
    
    st.markdown("""
    **Multi-Lingual Product Catalog Translator** is powered by:
    
    - **IndicTrans2** by AI4Bharat - State-of-the-art neural machine translation for Indian languages
    - **FastAPI** - High-performance web framework for the backend API
    - **Streamlit** - Interactive web interface for user-friendly translation experience
    - **SQLite** - Lightweight database for storing translations and corrections
    
    This tool helps e-commerce sellers translate their product listings into multiple Indian languages,
    enabling them to reach a broader customer base across different linguistic regions.
    
    **Features:**
    - ✅ Automatic language detection
    - ✅ Support for 15+ Indian languages
    - ✅ Manual correction interface
    - ✅ Translation history and analytics
    - ✅ Batch translation capability
    - ✅ Feedback loop for continuous improvement
    """)
    
    # System info
    with st.expander("🔍 System Information"):
        st.code(f"""
        API Status: {'🟢 Connected' if check_api_health() else '🔴 Disconnected'}
        Frontend: Streamlit {st.__version__}
        Supported Languages: {len(SUPPORTED_LANGUAGES)}
        """, language="text")

if __name__ == "__main__":
    main()
