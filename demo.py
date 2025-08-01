#!/usr/bin/env python3
"""
Medical Image Analyzer Demo Script
This script demonstrates the core functionality without the Streamlit interface.
"""

import numpy as np
from PIL import Image
import random
import json
from datetime import datetime

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
    confidence_text = f" Analysis confidence: {confidence:.1%}"
    
    return base_explanation + confidence_text

def create_sample_medical_image():
    """
    Create a sample medical image for demonstration
    """
    width, height = 256, 256
    
    # Create base image with medical scan-like appearance
    image = np.zeros((height, width), dtype=np.uint8)
    
    # Add some anatomical-like structures
    center_x, center_y = width // 2, height // 2
    radius = 80
    
    # Create circular region
    y, x = np.ogrid[:height, :width]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
    image[mask] = 180
    
    # Add some internal structures
    inner_radius = 50
    inner_mask = (x - center_x)**2 + (y - center_y)**2 <= inner_radius**2
    image[inner_mask] = 220
    
    # Add some "abnormalities"
    for i in range(2):
        offset_x = np.random.randint(-40, 40)
        offset_y = np.random.randint(-40, 40)
        small_radius = np.random.randint(8, 15)
        small_mask = (x - (center_x + offset_x))**2 + (y - (center_y + offset_y))**2 <= small_radius**2
        image[small_mask] = np.random.randint(100, 200)
    
    # Add noise
    noise = np.random.normal(0, 8, (height, width)).astype(np.uint8)
    image = np.clip(image + noise, 0, 255)
    
    return Image.fromarray(image)

def demo_analysis():
    """
    Run a complete demonstration of the medical image analysis
    """
    print("🏥 Medical Image Analyzer Demo")
    print("=" * 50)
    
    # Create sample image
    print("📸 Creating sample medical image...")
    sample_image = create_sample_medical_image()
    
    # Analyze the image
    print("🔍 Analyzing image...")
    severity, image_type, body_part, confidence = classify_image(sample_image)
    
    # Generate explanation
    explanation = generate_explanation(severity, image_type, body_part, confidence)
    
    # Display results
    print("\n📊 Analysis Results:")
    print("-" * 30)
    print(f"Severity: {severity}")
    print(f"Image Type: {image_type}")
    print(f"Body Part: {body_part}")
    print(f"Confidence: {confidence:.1%}")
    
    print("\n📝 Medical Explanation:")
    print("-" * 30)
    print(explanation)
    
    # Simulate translation
    print("\n🌐 Translation Demo:")
    print("-" * 30)
    languages = {
        "Hindi": "hi",
        "Spanish": "es", 
        "French": "fr"
    }
    
    for lang_name, lang_code in languages.items():
        print(f"{lang_name}: [Translation would be generated here]")
    
    # Simulate report generation
    print("\n📤 Report Generation Demo:")
    print("-" * 30)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report_data = {
        "timestamp": timestamp,
        "severity": severity,
        "image_type": image_type,
        "body_part": body_part,
        "confidence": confidence,
        "explanation": explanation,
        "languages_supported": list(languages.keys())
    }
    
    print("Report data structure:")
    print(json.dumps(report_data, indent=2))
    
    print("\n✅ Demo completed successfully!")
    print("\n🚀 To run the full application:")
    print("   ./run_app.sh")
    print("   or")
    print("   streamlit run medical_image_analyzer.py")

if __name__ == "__main__":
    demo_analysis()