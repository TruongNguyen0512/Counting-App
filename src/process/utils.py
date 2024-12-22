import cv2
import numpy as np

def load_image(image_path):
    """Load and preprocess image."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
    return img

def save_image(image, path):
    """Save image to disk."""
    cv2.imwrite(path, image)