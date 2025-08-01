#!/bin/bash

# Medical Image Analyzer Setup Script

echo "🏥 Medical Image Analyzer Setup"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "medical_env" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf medical_env
fi

python3 -m venv medical_env

# Activate virtual environment and install Python packages
echo "📥 Installing Python dependencies..."
source medical_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create sample medical image
echo "📸 Creating sample medical image..."
python create_sample_image.py

# Make launcher script executable
chmod +x run_app.sh

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To run the application:"
echo "   ./run_app.sh"
echo ""
echo "📱 Or manually:"
echo "   source medical_env/bin/activate"
echo "   streamlit run medical_image_analyzer.py"
echo ""
echo "🌐 Open your browser and go to: http://localhost:8501"
echo ""
echo "📁 Project files created:"
echo "   - medical_image_analyzer.py (main application)"
echo "   - requirements.txt (dependencies)"
echo "   - README.md (documentation)"
echo "   - sample_medical_image.png (test image)"
echo "   - run_app.sh (launcher script)"
echo ""