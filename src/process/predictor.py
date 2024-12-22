import tensorflow as tf
import numpy as np
import cv2

class ImagePredictor:
    def __init__(self, model_path='./best_model.keras'):
        """Initialize the predictor with a trained model."""
        self.model = tf.keras.models.load_model(model_path)
        
    def preprocess_slice(self, image_slice):
        """
        Preprocess a single 64x64 image slice.
        
        Args:
            image_slice: numpy array of shape (64, 64)
            
        Returns:
            preprocessed_slice: numpy array ready for model input
        """
        # Normalize the image
        normalized = image_slice.astype(float) / 255.0
        
        # Add batch and channel dimensions
        processed = np.expand_dims(normalized, axis=0)  # Add batch dimension
        processed = np.expand_dims(processed, axis=-1)  # Add channel dimension
        
        return processed
    
    def predict_slice(self, image_slice):
        """
        Make prediction for a single 64x64 image slice.
        
        Args:
            image_slice: numpy array of shape (64, 64)
            
        Returns:
            prediction: numpy array of shape (64, 64)
        """
        # Preprocess the slice
        processed_slice = self.preprocess_slice(image_slice)
        
        # Get prediction
        prediction = self.model.predict(processed_slice, verbose=0)
        
        # Remove batch and channel dimensions
        prediction = np.squeeze(prediction)
        
        return prediction
    
    def predict_batch(self, slices):
        """
        Make predictions for multiple image slices.
        
        Args:
            slices: list of numpy arrays, each of shape (64, 64)
            
        Returns:
            predictions: list of numpy arrays, each of shape (64, 64)
        """
        # Preprocess all slices
        processed_slices = np.stack([self.preprocess_slice(slice_img) for slice_img in slices])
        processed_slices = np.squeeze(processed_slices, axis=1)  # Remove extra batch dimension
        
        # Get predictions for all slices at once
        predictions = self.model.predict(processed_slices, verbose=0)
        
        # Convert to list of individual predictions
        predictions = [pred for pred in predictions]
        
        return predictions