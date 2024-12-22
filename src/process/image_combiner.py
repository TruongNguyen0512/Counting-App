import numpy as np

def combine_predictions(predictions, slice_positions, original_size, grid_size, slice_size=64):
    """
    Combine predicted 64x64 pieces back into a single image.
    
    Args:
        predictions: list of predicted image pieces
        slice_positions: list of (i, j) positions for each slice
        original_size: tuple of (height, width) of original image
        grid_size: tuple of (n_h, n_w) number of slices in each dimension
        slice_size: size of each square slice (default: 64)
    
    Returns:
        combined_image: reconstructed image of original size
    """
    n_h, n_w = grid_size
    height, width = original_size
    
    # Create empty array for combined image
    padded_height = n_h * slice_size
    padded_width = n_w * slice_size
    combined_image = np.zeros((padded_height, padded_width))
    
    # Place each prediction in the correct position
    for pred, (i, j) in zip(predictions, slice_positions):
        start_h = i * slice_size
        start_w = j * slice_size
        
        combined_image[start_h:start_h + slice_size, 
                      start_w:start_w + slice_size] = pred
    
    # Crop to original size
    combined_image = combined_image[:height, :width]
    
    return combined_image