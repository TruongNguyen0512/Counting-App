from tkinter import ttk, messagebox
import tkinter as tk
from process.pipeline import process_image_pipeline
import time
import threading

class ButtonFrame:
    def __init__(self, parent, root, camera_frame,process_animation):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=30)
        self.process_animation = process_animation
        # Store camera frame reference
        self.camera_frame = camera_frame
        
        # Add total count variable
        self.total_stripe_count = 0

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

    def _process_image(self, is_continue=False):
        """Common method for image processing with threading"""
        processing_done = threading.Event()
        result = {'error': None, 'stripe_count': None}

        def process_thread():
            try:
                image_path = self.camera_frame.capture_image()
                process_result = process_image_pipeline(image_path)
                result['stripe_count'] = process_result['stripe_count']
            except Exception as e:
                result['error'] = str(e)
            finally:
                processing_done.set()

        def animation_thread():
            try:
                self.process_animation.start()
                while not processing_done.is_set():
                    processing_done.wait(timeout=0.1)
            finally:
                self.process_animation.stop()
                self.frame.after(0, lambda: self.show_result(result, is_continue))

        process_t = threading.Thread(target=process_thread, daemon=True)
        anim_t = threading.Thread(target=animation_thread)
        
        process_t.start()
        anim_t.start()

    def counting(self):
        self._process_image(is_continue=False)

    def continue_action(self):
        self._process_image(is_continue=True)

    def show_result(self, result, is_continue=False):
        if result['error']:
            messagebox.showerror("Error", f"Processing failed: {result['error']}")
            print(f"Processing failed: {result['error']}")
        else:
            current_count = result['stripe_count']
            if is_continue:
                self.total_stripe_count += current_count
                messagebox.showinfo("Results", 
                    f"Number of new stripes: {current_count}\n"
                    f"Total stripes counted: {self.total_stripe_count}")
            else:
                self.total_stripe_count = current_count
                messagebox.showinfo("Results", 
                    f"Number of stripes detected: {current_count}")

    def process_captured_image(self, image_path):
        # This method can now be simplified since processing is done in counting
        print(f"Image captured at: {image_path}")
        
    def reset_action(self):
        self.total_stripe_count = 0
        messagebox.showinfo("Reset", "Counter has been reset to 0")