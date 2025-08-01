#!/bin/bash

# Medical Image Analyzer Launcher Script

echo "🏥 Starting Medical Image Analyzer..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "medical_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: python3 -m venv medical_env && source medical_env/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source medical_env/bin/activate

# Check if sample image exists, create if not
if [ ! -f "sample_medical_image.png" ]; then
    echo "📸 Creating sample medical image..."
    python create_sample_image.py
fi

# Run the Streamlit application
echo "🚀 Launching Medical Image Analyzer..."
echo "📱 Open your browser and go to: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

streamlit run medical_image_analyzer.py --server.port 8501 --server.address 0.0.0.0