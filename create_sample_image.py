import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_medical_image():
    """
    Create a sample medical image for testing purposes
    """
    # Create a grayscale image that looks like a medical scan
    width, height = 512, 512
    
    # Create base image with medical scan-like appearance
    image = np.zeros((height, width), dtype=np.uint8)
    
    # Add some anatomical-like structures
    # Central region (like brain or organ)
    center_x, center_y = width // 2, height // 2
    radius = 150
    
    # Create circular region
    y, x = np.ogrid[:height, :width]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
    image[mask] = 180
    
    # Add some internal structures
    inner_radius = 100
    inner_mask = (x - center_x)**2 + (y - center_y)**2 <= inner_radius**2
    image[inner_mask] = 220
    
    # Add some "abnormalities" or structures
    # Small circular regions
    for i in range(3):
        offset_x = np.random.randint(-80, 80)
        offset_y = np.random.randint(-80, 80)
        small_radius = np.random.randint(10, 25)
        small_mask = (x - (center_x + offset_x))**2 + (y - (center_y + offset_y))**2 <= small_radius**2
        image[small_mask] = np.random.randint(100, 200)
    
    # Add some noise to make it look more realistic
    noise = np.random.normal(0, 10, (height, width)).astype(np.uint8)
    image = np.clip(image + noise, 0, 255)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image)
    
    # Add some text to make it look more medical
    draw = ImageDraw.Draw(pil_image)
    
    # Try to use a medical-looking font, fallback to default if not available
    try:
        # Try to use a system font that might be available
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
    
    # Add medical scan labels
    draw.text((10, 10), "MEDICAL SCAN", fill=255, font=font)
    draw.text((10, height - 30), "Sample Image", fill=255, font=font)
    
    # Add some scan lines or grid
    for i in range(0, width, 50):
        draw.line([(i, 0), (i, height)], fill=100, width=1)
    for i in range(0, height, 50):
        draw.line([(0, i), (width, i)], fill=100, width=1)
    
    return pil_image

if __name__ == "__main__":
    # Create sample image
    sample_image = create_sample_medical_image()
    
    # Save the image
    sample_image.save("sample_medical_image.png")
    print("Sample medical image created: sample_medical_image.png")
    print("You can use this image to test the Medical Image Analyzer application.")