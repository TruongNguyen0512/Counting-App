import cv2
import numpy as np

class StripeCounter:
    def __init__(self):
        self.min_stripe_length = 50  # Minimum length to consider as valid stripe
    
    def count_stripes(self, skeleton_image):
        """Count number of white stripes in skeletonized image"""
        # Ensure binary image
        _, binary = cv2.threshold(skeleton_image, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by length
        valid_stripes = []
        for contour in contours:
            # Calculate contour length
            length = cv2.arcLength(contour, False)
            if length >= self.min_stripe_length:
                valid_stripes.append(contour)
        
        # Draw results on debug image
        debug_image = cv2.cvtColor(skeleton_image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(debug_image, valid_stripes, -1, (0,255,0), 2)
        
        # Save debug image
        cv2.imwrite('stripe_detection_debug.png', debug_image)
        
        return len(valid_stripes), debug_image

    def set_min_stripe_length(self, length):
        """Adjust minimum stripe length threshold"""
        self.min_stripe_length = length
