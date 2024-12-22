import cv2
import numpy as np

def convert_to_grayscale(image):
    """
    Convert image to grayscale if it's not already.
    
    Args:
        image: numpy array of shape (height, width) or (height, width, channels)
    
    Returns:
        grayscale_image: numpy array of shape (height, width)
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def normalize_image(image):
    """
    Normalize image values to range [0, 1].
    
    Args:
        image: numpy array of grayscale image
    
    Returns:
        normalized_image: numpy array with values between 0 and 1
    """
    return image.astype(float) / 255.0

def preprocess_image(image):
    """
    Preprocess image by converting to grayscale and normalizing.
    
    Args:
        image: numpy array of input image
        
    Returns:
        processed_image: preprocessed grayscale image
    """
    # Convert to grayscale
    gray_image = convert_to_grayscale(image)
    
    # Normalize pixel values
    normalized_image = normalize_image(gray_image)
    
    return normalized_image