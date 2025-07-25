# Streamlit Cloud entry point
import streamlit as st
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

# Import the cloud backend
from cloud_backend import cloud_service

# Configure Streamlit page
st.set_page_config(
    page_title="Multi-Lingual Catalog Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def main():
    """Main Streamlit application for cloud deployment"""
    
    # Header with cloud demo notice
    st.title("🌐 Multi-Lingual Product Catalog Translator")
    st.markdown("### Powered by IndicTrans2 by AI4Bharat")
    
    # Cloud demo banner
    st.warning("""
    🌟 **Cloud Demo Version** 
    
    This is a demonstration version running on Streamlit Cloud with simulated AI responses. 
    The full version with real IndicTrans2 models can be deployed on infrastructure with GPU support.
    
    ✨ **Features demonstrated**: Product translation, multi-language support, quality scoring, correction workflow
    """)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["🏠 Translate Product", "📊 Translation History", "📈 Analytics", "⚙️ About"]
    )
    
    if page == "🏠 Translate Product":
        translate_product_page()
    elif page == "📊 Translation History":
        translation_history_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "⚙️ About":
        about_page()

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
                default=["hi", "ta"],
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

def process_translations(title: str, description: str, category: str, source_lang: str, target_languages: list):
    """Process translations for product fields"""
    
    translations = {}
    
    # Detect source language if auto-detect is selected
    if source_lang == "auto-detect":
        detection_result = cloud_service.detect_language(title)
        source_lang = detection_result.get("language", "en")
        st.info(f"🔍 Detected source language: {SUPPORTED_LANGUAGES.get(source_lang, source_lang)}")
    
    # Translate to each target language
    for target_lang in target_languages:
        if target_lang == source_lang:
            continue
        
        translations[target_lang] = {}
        
        # Translate title
        title_result = cloud_service.translate(title, source_lang, target_lang)
        translations[target_lang]["title"] = title_result
        
        # Translate description
        description_result = cloud_service.translate(description, source_lang, target_lang)
        translations[target_lang]["description"] = description_result
        
        # Translate category if provided
        if category:
            category_result = cloud_service.translate(category, source_lang, target_lang)
            translations[target_lang]["category"] = category_result
    
    return translations

def display_translations(translations: dict, original_title: str, original_description: str, original_category: str):
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
                        result = cloud_service.submit_correction(translation_id, corrected_title, "Title correction")
                        st.success("✅ Correction saved successfully!")
            
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
                        result = cloud_service.submit_correction(translation_id, corrected_description, "Description correction")
                        st.success("✅ Correction saved successfully!")
            
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
                        result = cloud_service.submit_correction(translation_id, corrected_category, "Category correction")
                        st.success("✅ Correction saved successfully!")
            
            st.markdown("---")

def translation_history_page():
    """Translation history page"""
    
    st.header("📊 Translation History")
    
    # Fetch translation history
    history = cloud_service.get_history()
    
    if not history:
        st.info("No translation history available yet.")
        return
    
    # Display history
    for record in history:
        with st.expander(f"Translation #{record['id']} - {record['source_language']} → {record['target_language']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original:**")
                st.write(record["original_text"])
                
            with col2:
                st.markdown("**Translation:**")
                st.write(record["translated_text"])
                
            st.caption(f"Confidence: {record['model_confidence']:.2%} | Created: {record['created_at'][:19]}")

def analytics_page():
    """Analytics and statistics page"""
    
    st.header("📈 Analytics & Statistics")
    
    # Get history for analytics
    history = cloud_service.get_history()
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Translations", len(history))
    
    with col2:
        corrected = sum(1 for h in history if h.get("corrected_text"))
        st.metric("Corrections Submitted", corrected)
    
    with col3:
        st.metric("Languages Supported", len(SUPPORTED_LANGUAGES))
    
    with col4:
        if history:
            avg_confidence = sum(h["model_confidence"] for h in history) / len(history)
            st.metric("Avg. Confidence", f"{avg_confidence:.1%}")
    
    # Language usage chart
    if history:
        st.subheader("🔀 Language Usage")
        
        import pandas as pd
        
        # Count language pairs
        lang_pairs = {}
        for h in history:
            pair = f"{h['source_language']} → {h['target_language']}"
            lang_pairs[pair] = lang_pairs.get(pair, 0) + 1
        
        if lang_pairs:
            df = pd.DataFrame(list(lang_pairs.items()), columns=["Language Pair", "Count"])
            st.bar_chart(df.set_index("Language Pair"))

def about_page():
    """About and settings page"""
    
    st.header("⚙️ About This Demo")
    
    st.markdown("""
    ## 🌟 Multi-Lingual Product Catalog Translator
    
    **This is a cloud demonstration of an AI-powered translation system for e-commerce.**
    
    ### 🎯 **Purpose:**
    - Help e-commerce sellers translate product listings into multiple Indian languages
    - Reach customers in their native languages
    - Improve accessibility and market reach
    
    ### 🔧 **Technology Stack:**
    - **AI Models**: IndicTrans2 by AI4Bharat (in full version)
    - **Backend**: FastAPI with async operations
    - **Frontend**: Streamlit for interactive UI
    - **Database**: SQLite for translation storage
    - **Languages**: 15+ Indian languages + English
    
    ### ✨ **Key Features:**
    - **Real AI Translation** (in full version with IndicTrans2 models)
    - **Product-specific optimization** for e-commerce
    - **Multi-language support** for Indian market
    - **Quality control** with confidence scoring
    - **Human feedback loop** for continuous improvement
    - **Translation history** and analytics
    - **Batch processing** capabilities
    
    ### 🚀 **Production Deployment:**
    The full version can be deployed on:
    - **Cloud platforms** (AWS, GCP, Azure) with GPU support
    - **Docker containers** for scalability
    - **Kubernetes** for production workloads
    - **Local servers** with high-performance hardware
    
    ### 📊 **Business Value:**
    - **Market Expansion**: Reach regional customers
    - **User Experience**: Native language shopping
    - **SEO Benefits**: Localized content
    - **Cost Efficiency**: Automated translation workflow
    
    ### 🎓 **Perfect for:**
    - **E-commerce platforms** like Meesho, Flipkart, Amazon India
    - **Regional marketplaces** serving diverse linguistic markets
    - **Content localization** for Indian languages
    - **Cross-border commerce** in South Asia
    """)
    
    # System info
    st.subheader("💻 Demo Environment")
    st.info("""
    **Current Setup:**
    - Platform: Streamlit Community Cloud
    - Translation: Simulated responses for demo
    - Languages: 15+ Indian languages supported
    - Storage: In-memory (resets on restart)
    
    **Full Version Features:**
    - Real IndicTrans2 neural translation models
    - Persistent database storage
    - GPU acceleration support
    - Production-grade API endpoints
    - Advanced analytics and monitoring
    """)

if __name__ == "__main__":
    main()
