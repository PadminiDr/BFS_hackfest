import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
import json
from datetime import datetime
import os
import tempfile

# For translation
try:
    from googletrans import Translator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("Translation feature requires googletrans library. Install with: pip install googletrans==4.0.0rc1")

# For text-to-speech
try:
    from gtts import gTTS
    import pygame
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    st.warning("Text-to-speech feature requires gtts and pygame libraries. Install with: pip install gtts pygame")

# For PDF export
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning("PDF export requires reportlab library. Install with: pip install reportlab")

# Set page config
st.set_page_config(
    page_title="Medical Image Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 1rem 0;
    }
    .severity-normal { border-left-color: #28a745 !important; }
    .severity-mild { border-left-color: #ffc107 !important; }
    .severity-severe { border-left-color: #dc3545 !important; }
    .upload-area {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
    }
    .language-selector {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'annotated_image' not in st.session_state:
    st.session_state.annotated_image = None

def classify_image(image):
    """
    Simulate medical image classification
    Returns: severity, image_type, body_part, confidence
    """
    # Set random seed for reproducibility
    random.seed(hash(image.tobytes()) % 1000)
    
    severities = ["Normal", "Mild", "Severe"]
    image_types = ["MRI", "CT Scan", "X-Ray"]
    body_parts = ["Brain", "Lungs", "Oral Cavity", "Larynx", "Chest", "Abdomen"]
    
    # Simulate classification with some bias towards medical conditions
    severity = random.choices(severities, weights=[0.3, 0.4, 0.3])[0]
    image_type = random.choice(image_types)
    body_part = random.choice(body_parts)
    confidence = random.uniform(0.75, 0.95)
    
    return severity, image_type, body_part, confidence

def generate_explanation(severity, image_type, body_part, confidence):
    """
    Generate layman-friendly explanation based on classification results
    """
    explanations = {
        "Normal": f"This {image_type.lower()} scan of the {body_part.lower()} appears to be within normal limits. No significant abnormalities were detected. The scan quality is good and shows typical anatomical structures.",
        "Mild": f"This {image_type.lower()} scan shows some mild abnormalities in the {body_part.lower()} area. While not immediately concerning, follow-up monitoring may be recommended. The changes are subtle and could be due to various factors.",
        "Severe": f"This {image_type.lower()} scan reveals significant abnormalities in the {body_part.lower()} that require immediate medical attention. The findings suggest a serious condition that needs prompt evaluation by a healthcare professional."
    }
    
    base_explanation = explanations.get(severity, "Analysis complete.")
    
    # Add confidence level
    confidence_text = f" Analysis confidence: {confidence:.1%}"
    
    return base_explanation + confidence_text

def annotate_image(image, severity, body_part):
    """
    Add colored overlay to mark areas of interest
    """
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Create a copy for annotation
    annotated = img_array.copy()
    
    # Define colors for different severities
    colors = {
        "Normal": (0, 255, 0, 128),    # Green
        "Mild": (255, 255, 0, 128),    # Yellow
        "Severe": (255, 0, 0, 128)     # Red
    }
    
    color = colors.get(severity, (0, 255, 0, 128))
    
    # Create overlay
    overlay = np.zeros_like(img_array)
    
    # Add colored rectangle overlay
    height, width = img_array.shape[:2]
    cv2.rectangle(overlay, (width//4, height//4), (3*width//4, 3*height//4), color[:3], -1)
    
    # Blend overlay with original image
    alpha = 0.3
    annotated = cv2.addWeighted(annotated, 1-alpha, overlay, alpha, 0)
    
    # Add text annotation
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"{severity} - {body_part}"
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    
    # Calculate text position
    text_x = (width - text_size[0]) // 2
    text_y = height - 50
    
    # Add background rectangle for text
    cv2.rectangle(annotated, (text_x-10, text_y-text_size[1]-10), 
                 (text_x+text_size[0]+10, text_y+10), (0, 0, 0), -1)
    
    # Add text
    cv2.putText(annotated, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
    
    return Image.fromarray(annotated)

def translate_text(text, target_language):
    """
    Translate text to target language
    """
    if not TRANSLATION_AVAILABLE:
        return text
    
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

def text_to_speech(text, language):
    """
    Convert text to speech
    """
    if not TTS_AVAILABLE:
        st.error("Text-to-speech not available")
        return None
    
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

def export_report(severity, image_type, body_part, explanation, translated_text, language):
    """
    Export analysis report as text or PDF
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create report content
    report_content = f"""
MEDICAL IMAGE ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

ANALYSIS RESULTS:
- Severity: {severity}
- Image Type: {image_type}
- Body Part: {body_part}

EXPLANATION:
{explanation}

TRANSLATED SUMMARY ({language}):
{translated_text}

---
This report was generated by Medical Image Analyzer
For medical decisions, always consult with qualified healthcare professionals.
    """
    
    return report_content, timestamp

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Medical Image Analyzer</h1>
        <p>AI-Powered Medical Image Analysis with Multi-Language Support</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for language selection
    st.sidebar.title("🌐 Language Settings")
    
    languages = {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh",
        "Japanese": "ja",
        "Arabic": "ar"
    }
    
    selected_language = st.sidebar.selectbox(
        "Select Language for Translation:",
        list(languages.keys()),
        index=0
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Upload Medical Image")
        
        uploaded_file = st.file_uploader(
            "Choose a medical image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload MRI, CT scan, or X-ray images"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.session_state.uploaded_image = image
            
            # Analyze button
            if st.button("🔍 Analyze Image", type="primary"):
                with st.spinner("Analyzing image..."):
                    # Classify image
                    severity, image_type, body_part, confidence = classify_image(image)
                    
                    # Generate explanation
                    explanation = generate_explanation(severity, image_type, body_part, confidence)
                    
                    # Annotate image
                    annotated_image = annotate_image(image, severity, body_part)
                    
                    # Store results
                    st.session_state.analysis_results = {
                        'severity': severity,
                        'image_type': image_type,
                        'body_part': body_part,
                        'confidence': confidence,
                        'explanation': explanation
                    }
                    st.session_state.annotated_image = annotated_image
                    
                    st.success("Analysis complete!")
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Display results in styled cards
            severity_class = f"severity-{results['severity'].lower()}"
            
            st.markdown(f"""
            <div class="result-card {severity_class}">
                <h4>🔍 Classification Results</h4>
                <p><strong>Severity:</strong> {results['severity']}</p>
                <p><strong>Image Type:</strong> {results['image_type']}</p>
                <p><strong>Body Part:</strong> {results['body_part']}</p>
                <p><strong>Confidence:</strong> {results['confidence']:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display annotated image
            if st.session_state.annotated_image:
                st.image(st.session_state.annotated_image, caption="Annotated Image", use_column_width=True)
            
            # Explanation section
            st.markdown("""
            <div class="result-card">
                <h4>📝 Medical Explanation</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.write(results['explanation'])
            
            # Translation section
            if TRANSLATION_AVAILABLE:
                st.markdown("""
                <div class="language-selector">
                    <h4>🌐 Translation</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Translate to {selected_language}"):
                    with st.spinner("Translating..."):
                        translated_text = translate_text(results['explanation'], languages[selected_language])
                        st.session_state.translated_text = translated_text
                        st.success(f"Translated to {selected_language}")
                
                if 'translated_text' in st.session_state:
                    st.write(f"**{selected_language} Translation:**")
                    st.write(st.session_state.translated_text)
                    
                    # Text-to-speech
                    if TTS_AVAILABLE:
                        if st.button(f"🔊 Listen to {selected_language} Audio"):
                            with st.spinner("Generating audio..."):
                                audio_file = text_to_speech(st.session_state.translated_text, languages[selected_language])
                                if audio_file:
                                    with open(audio_file, 'rb') as f:
                                        audio_bytes = f.read()
                                    st.audio(audio_bytes, format='audio/mp3')
                                    # Clean up temporary file
                                    os.unlink(audio_file)
            
            # Export section
            st.markdown("""
            <div class="result-card">
                <h4>📤 Export Report</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("📄 Export as TXT"):
                    report_content, timestamp = export_report(
                        results['severity'],
                        results['image_type'],
                        results['body_part'],
                        results['explanation'],
                        st.session_state.get('translated_text', 'No translation available'),
                        selected_language
                    )
                    
                    st.download_button(
                        label="Download TXT Report",
                        data=report_content,
                        file_name=f"medical_analysis_report_{timestamp}.txt",
                        mime="text/plain"
                    )
            
            with col_export2:
                if PDF_AVAILABLE and st.button("📋 Export as PDF"):
                    report_content, timestamp = export_report(
                        results['severity'],
                        results['image_type'],
                        results['body_part'],
                        results['explanation'],
                        st.session_state.get('translated_text', 'No translation available'),
                        selected_language
                    )
                    
                    # Create PDF
                    pdf_buffer = io.BytesIO()
                    p = canvas.Canvas(pdf_buffer, pagesize=letter)
                    width, height = letter
                    
                    # Add content to PDF
                    y_position = height - 50
                    for line in report_content.split('\n'):
                        if line.strip():
                            p.drawString(50, y_position, line)
                            y_position -= 20
                    
                    p.save()
                    pdf_buffer.seek(0)
                    
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_buffer.getvalue(),
                        file_name=f"medical_analysis_report_{timestamp}.pdf",
                        mime="application/pdf"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>⚠️ Disclaimer:</strong> This application is for educational and demonstration purposes only. 
        Medical decisions should always be made by qualified healthcare professionals.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()