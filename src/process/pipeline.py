from .predictor import ImagePredictor
from .skeleton_converter import SkeletonConverter
from .counting import StripeCounter  # Fixed: removed .process
from .image_slicer import slice_image
from .image_combiner import combine_predictions
from .utils import load_image, save_image
from .preprocess import preprocess_image, convert_to_grayscale
import os

def process_image_pipeline(image_path, model_path='./best_model_0.2.keras'):
    """
    Complete pipeline: load -> preprocess -> slice -> predict -> combine -> skeletonize -> count
    """
    if not isinstance(image_path, str):
        raise ValueError(f"Expected string path, got {type(image_path)}")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    # Load image
    image = load_image(image_path)
    
    # Preprocess image
    print("Preprocessing image...")
    gray_image = convert_to_grayscale(image)
    preprocessed_image = preprocess_image(gray_image)
    
    # Save preprocessed image for debugging
    base_path = image_path.replace('.jpg', '')
    save_image(f"{base_path}_preprocessed.png", preprocessed_image)
    
    # Slice preprocessed image
    slices, slice_positions, original_size, grid_size = slice_image(preprocessed_image)
    
    # Make predictions
    predictor = ImagePredictor(model_path)
    predictions = predictor.predict_batch(slices)
    
    # Combine predictions
    combined_image = combine_predictions(
        predictions, 
        slice_positions, 
        original_size, 
        grid_size
    )
    
    # Convert to skeleton
    skeleton_converter = SkeletonConverter()
    skeleton = skeleton_converter.convert_to_skeleton(combined_image)
    
    # Count stripes
    counter = StripeCounter()
    stripe_count, debug_image = counter.count_stripes(skeleton)
    
    # Save output images
    skeleton_converter.save_comparison(combined_image, skeleton, f'{base_path}_skeleton_comparison.png')
    save_image(f'{base_path}_stripe_detection.png', debug_image)
    
    print(f"Number of stripes detected: {stripe_count}")
    
    return {
        'stripe_count': stripe_count,
        'debug_image': debug_image
    }