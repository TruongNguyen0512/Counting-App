from tkinter import ttk
import tkinter as tk
import sys
import os
import threading
import time

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from process.pipeline import process_image_pipeline
from .process_animation import ProcessAnimation

class ButtonFrame:
    def __init__(self, parent, root, camera_frame, process_animation):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=30)
        
        # Store references
        self.camera_frame = camera_frame
        self.process_animation = process_animation  # Use the passed animation instance
        
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
        self.predict_output = 0  

        # Pack buttons with more spacing
        for button in self.buttons.values():
            button.pack(side='left', padx=20)

    def counting(self):
        def process():
            try:
                # Start animation in main thread
                self.frame.after(1, lambda: [
                    print("Starting animation..."),
                    self.process_animation.start()
                ])
                 
                # Process image in background while animation is running
                print("Capturing image...")
                image_path = self.camera_frame.capture_image()
                if image_path:
                    print("Processing image...")
                    result = process_image_pipeline(image_path)
                    stripe_count = result['stripe_count']
                    print(f"Found {stripe_count} stripes")
                    
                    # Stop animation only after processing is complete
                    self.frame.after(1, lambda: [
                        print("Processing complete, stopping animation..."),
                        self.process_animation.stop()
                    ])
                    
                    # Re-enable button after processing
                    self.frame.after(100, lambda: 
                        self.buttons['count'].configure(state='normal')
                    )
            except Exception as e:
                print(f"Error during counting: {e}")
                # Stop animation and re-enable button on error
                self.frame.after(1, lambda: [
                    self.process_animation.stop(),
                    self.buttons['count'].configure(state='normal')
                ])

        # Disable count button
        self.buttons['count'].configure(state='disabled')
        
        # Start processing in separate thread
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()

    def process_captured_image(self, image_path):
        # This method will be called after image capture
        print(f"Processing captured image: {image_path}")
        # Add your counting logic here
        
    def continue_action(self):
        # using the pipeline to process the image
        image_path = self.camera_frame.capture_image()
                if image_path:
                    print("Processing image...")
                    result = process_image_pipeline(image_path)
                    stripe_count = result['stripe_count']
                    print(f"Found {stripe_count} stripes")
                    self.predict_output = stripe_count + self.predict_output
                    print(f"Total stripes: {self.predict_output}")
        return self.predict_output

        
    def reset_action(self):
        pass