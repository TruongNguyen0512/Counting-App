from tkinter import ttk
import tkinter as tk
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from process.pipeline import process_image_pipeline
from .process_animation import ProcessAnimation

class ButtonFrame:
    def __init__(self, parent, root, camera_frame, process_animation):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=30)
        
        # Store camera frame reference
        self.camera_frame = camera_frame
        
        # Set up the counting callback
        self.camera_frame.set_count_callback(self.process_captured_image)

        # Create a style for bigger buttons
        style = ttk.Style()
        style.configure('Big.TButton', 
                       padding=(20, 10),
                       font=('Helvetica', 30, 'bold'))

        # Create buttons with the new style
        self.buttons = {
            'count': ttk.Button(
                self.frame, 
                text="Count", 
                command=self.counting,
                style='Big.TButton'
            ),
            'continue': ttk.Button(
                self.frame, 
                text="Continue", 
                command=self.continue_action,
                style='Big.TButton'
            ),
            'reset': ttk.Button(
                self.frame, 
                text="Reset", 
                command=self.reset_action,
                style='Big.TButton'
            ),
            'exit': ttk.Button(
                self.frame, 
                text="Exit", 
                command=root.quit,
                style='Big.TButton'
            )
        }

        # Pack buttons with more spacing
        for button in self.buttons.values():
            button.pack(side='left', padx=20)

        self.parent = parent
        self.process_animation = ProcessAnimation(parent)

    def counting(self):
        # Start animation
        self.process_animation.start()
        
        try:
            # Capture image and process
            image_path = self.camera_frame.capture_image()
            if image_path:
                result = process_image_pipeline(image_path)
                stripe_count = result['stripe_count']
                return stripe_count
        finally:
            # Stop animation when done
            self.process_animation.stop()

    def process_captured_image(self, image_path):
        # This method will be called after image capture
        print(f"Processing captured image: {image_path}")
        # Add your counting logic here
        
    def continue_action(self):
        pass

    def reset_action(self):
        pass