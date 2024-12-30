import cv2
import numpy as np

class StripeCounter:
    def __init__(self):
        self.min_stripe_length = 50  # Minimum length to consider as valid stripe
        self.min_stripe_area = 100   # Minimum area to consider as valid stripe
    
    def count_stripes(self, skeleton_image):
        """Count number of white stripes in skeletonized image"""
        # Ensure binary image
        _, binary = cv2.threshold(skeleton_image, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by length and area
        valid_stripes = []
        for i, contour in enumerate(contours):
            # Calculate contour length and area
            length = cv2.arcLength(contour, False)
            area = cv2.contourArea(contour)
            
            if length >= self.min_stripe_length and area >= self.min_stripe_area:
                valid_stripes.append(contour)
                
        # Draw results on debug image
        debug_image = cv2.cvtColor(skeleton_image, cv2.COLOR_GRAY2BGR)
        
        # Draw all contours in red
        cv2.drawContours(debug_image, contours, -1, (0,0,255), 1)
        
        # Draw valid stripes in green with numbers
        for i, contour in enumerate(valid_stripes):
            cv2.drawContours(debug_image, [contour], -1, (0,255,0), 2)
            # Get contour center for numbering
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Draw stripe number
                cv2.putText(debug_image, str(i+1), (cx-10, cy), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        # Print debug info
        print(f"Total contours found: {len(contours)}")
        print(f"Valid stripes after filtering: {len(valid_stripes)}")
        print(f"Length threshold: {self.min_stripe_length}")
        print(f"Area threshold: {self.min_stripe_area}")
        
        return len(valid_stripes), debug_image

    def set_min_stripe_length(self, length):
        """Adjust minimum stripe length threshold"""
        self.min_stripe_length = length
        
    def set_min_stripe_area(self, area):
        """Adjust minimum stripe area threshold"""
        self.min_stripe_area = area
