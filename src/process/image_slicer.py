import numpy as np
import cv2
from .preprocess import convert_to_grayscale

def slice_image(image, slice_size=64):
    """
    Slice an image into 64x64 pieces.
    
    Args:
        image: numpy array of shape (height, width) or (height, width, channels)
        slice_size: size of each square slice (default: 64)
    
    Returns:
        slices: list of image slices
        original_size: tuple of (height, width) of original image
    """
    # Ensure image is grayscale
    image = convert_to_grayscale(image)
    
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    height, width = image.shape
    
    # Calculate padding if needed
    pad_height = slice_size - (height % slice_size) if height % slice_size != 0 else 0
    pad_width = slice_size - (width % slice_size) if width % slice_size != 0 else 0
    
    # Pad image if necessary
    if pad_height > 0 or pad_width > 0:
        image = np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant')
    
    # Calculate number of slices in each dimension
    n_h = (height + pad_height) // slice_size
    n_w = (width + pad_width) // slice_size
    
    # Create list to store slices
    slices = []
    slice_positions = []
    
    # Slice the image
    for i in range(n_h):
        for j in range(n_w):
            start_h = i * slice_size
            start_w = j * slice_size
            
            slice_img = image[start_h:start_h + slice_size, 
                            start_w:start_w + slice_size]
            
            slices.append(slice_img)
            slice_positions.append((i, j))
    
    return slices, slice_positions, (height, width), (n_h, n_w)