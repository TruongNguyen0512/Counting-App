from tkinter import ttk
import tkinter as tk

class ButtonFrame:
    def __init__(self, parent, root, camera_frame):
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

    def counting(self):
        # Trigger image capture when Count button is pressed
        self.camera_frame.capture_image()
    
    def process_captured_image(self, image_path):
        # This method will be called after image capture
        print(f"Processing captured image: {image_path}")
        # Add your counting logic here
        
    def continue_action(self):
        pass

    def reset_action(self):
        pass