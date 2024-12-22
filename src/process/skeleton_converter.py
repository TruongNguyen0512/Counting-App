import cv2
import numpy as np
import matplotlib.pyplot as plt

class SkeletonConverter:
    def __init__(self):
        self.kernel = np.ones((3, 3), np.uint8)

    def convert_to_skeleton(self, image):
        """
        Convert an image to its skeletal form.
        
        Args:
            image: numpy array of grayscale image
            
        Returns:
            skeleton: numpy array of skeletonized image
        """
        # Convert to binary if not already
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        
        # Create empty skeleton
        skeleton = np.zeros_like(binary_image)
        
        # Iterative skeletonization
        while True:
            eroded = cv2.erode(binary_image, self.kernel)
            dilated = cv2.dilate(eroded, self.kernel)
            skeleton_part = cv2.subtract(binary_image, dilated)
            skeleton = cv2.bitwise_or(skeleton, skeleton_part)
            binary_image = eroded
            
            if cv2.countNonZero(binary_image) == 0:
                break
                
        return skeleton

    def save_comparison(self, original, skeleton, output_path):
        """
        Save comparison of original and skeletonized images.
        
        Args:
            original: original image array
            skeleton: skeletonized image array
            output_path: path to save the comparison image
        """
        plt.figure(figsize=(10, 5))
        
        plt.subplot(1, 2, 1)
        plt.title('Original Image')
        plt.imshow(original, cmap='gray')
        
        plt.subplot(1, 2, 2)
        plt.title('Skeletonized Image')
        plt.imshow(skeleton, cmap='gray')
        
        plt.savefig(output_path)
        plt.close()