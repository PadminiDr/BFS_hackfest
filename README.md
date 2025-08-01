# 🏥 Medical Image Analyzer

A comprehensive Streamlit application for AI-powered medical image analysis with multi-language support, text-to-speech, and report generation capabilities.

## 🌟 Features

### 📥 Image Upload & Display
- Support for medical image formats (JPG, JPEG, PNG)
- Real-time image preview
- Optimized for MRI, CT scans, and X-ray images

### 🧠 AI-Powered Analysis
- **Severity Classification**: Normal, Mild, or Severe
- **Image Type Detection**: MRI, CT Scan, X-Ray
- **Body Part Identification**: Brain, Lungs, Oral Cavity, Larynx, Chest, Abdomen
- **Confidence Scoring**: AI confidence levels for each prediction

### 🎨 Visual Annotation
- **Color-coded Overlays**:
  - 🟢 Green: Normal findings
  - 🟡 Yellow: Mild abnormalities
  - 🔴 Red: Severe conditions
- Automatic text annotation on images
- Professional medical imaging-style overlays

### 📝 Intelligent Explanations
- Layman-friendly medical explanations
- Context-aware descriptions based on severity
- Confidence level reporting
- Professional medical terminology simplified

### 🌐 Multi-Language Support
- **Translation Languages**:
  - English, Hindi, Tamil
  - Spanish, French, German
  - Chinese, Japanese, Arabic
- Google Translate API integration
- Real-time translation with error handling

### 🔊 Text-to-Speech
- Audio generation in selected languages
- Browser-based audio playback
- High-quality speech synthesis
- Support for multiple languages

### 📤 Report Export
- **TXT Export**: Plain text reports with timestamps
- **PDF Export**: Professional PDF reports with formatting
- Comprehensive analysis summaries
- Translated content inclusion

### 🎨 Modern UI/UX
- Responsive design with columns layout
- Color-coded severity indicators
- Professional medical interface
- Mobile-friendly design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run medical_image_analyzer.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📋 Usage Guide

### Step 1: Upload Image
- Click "Browse files" in the upload section
- Select a medical image (JPG, JPEG, PNG)
- The image will be displayed in the interface

### Step 2: Analyze Image
- Click the "🔍 Analyze Image" button
- Wait for the AI analysis to complete
- View results in the right panel

### Step 3: Review Results
- Check severity classification (color-coded)
- Review image type and body part identification
- Examine the annotated image with overlays
- Read the medical explanation

### Step 4: Translation & Audio
- Select target language from the sidebar
- Click "Translate" to get localized explanation
- Use "Listen to Audio" for text-to-speech

### Step 5: Export Report
- Choose between TXT or PDF format
- Download comprehensive analysis report
- Share with healthcare professionals

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Image Processing**: OpenCV and PIL
- **AI Simulation**: Reproducible random classification
- **Translation**: Google Translate API
- **TTS**: Google Text-to-Speech (gTTS)
- **PDF Generation**: ReportLab

### Key Functions
- `classify_image()`: Simulates AI classification
- `annotate_image()`: Adds visual overlays
- `generate_explanation()`: Creates medical explanations
- `translate_text()`: Handles language translation
- `text_to_speech()`: Converts text to audio
- `export_report()`: Generates downloadable reports

### Session Management
- Persistent state across interactions
- Image caching and result storage
- Translation memory

## ⚠️ Important Notes

### Medical Disclaimer
This application is designed for **educational and demonstration purposes only**. 
- Not intended for actual medical diagnosis
- Always consult qualified healthcare professionals
- Results are simulated and not medically validated

### Dependencies
Some features require internet connectivity:
- Translation services
- Text-to-speech generation
- Google Translate API

### Performance
- Image processing optimized for medical images
- Caching implemented for better performance
- Responsive design for various screen sizes

## 🛠️ Customization

### Adding New Languages
Edit the `languages` dictionary in the main function:
```python
languages = {
    "Your Language": "language_code",
    # Add more languages here
}
```

### Modifying Classification
Update the `classify_image()` function to integrate with real ML models:
```python
def classify_image(image):
    # Replace simulation with actual model inference
    # model = load_your_model()
    # results = model.predict(image)
    pass
```

### Custom Styling
Modify the CSS in the `st.markdown()` section to customize the appearance.

## 📁 Project Structure
```
medical_image_analyzer/
├── medical_image_analyzer.py  # Main application
├── requirements.txt           # Dependencies
├── README.md                 # This file
└── .streamlit/               # Streamlit configuration
    └── config.toml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please ensure compliance with local regulations regarding medical software.

## 🆘 Support

For issues or questions:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure internet connectivity for translation/TTS features
4. Check image format compatibility

---

**Built with ❤️ for medical education and research**