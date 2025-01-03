from tkinter import ttk, messagebox
import tkinter as tk
from process.pipeline import process_image_pipeline
from .counter_display import CounterDisplay
import threading
import time
from ..theme import AppTheme

class ButtonFrame:
    def __init__(self, parent, root, camera_frame, process_animation):
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(side='bottom', pady=(0, 50),padx=(150,0))  # Add bottom padding
        
        # Create center frame for buttons
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(expand=True)
        
        # Store references and setup
        self.counter_display = CounterDisplay(parent)
        self.process_animation = process_animation
        self.camera_frame = camera_frame
        self.total_stripe_count = 0
        self.camera_frame.set_count_callback(self.process_captured_image)

        # Configure styles using theme
        style = ttk.Style()
        AppTheme.configure_styles(style)

        # Create buttons with themed styles
        self.buttons = {
            'count': ttk.Button(
                self.button_frame, 
                text="Count", 
                command=self.counting,
                style='Count.TButton'
            ),
            'continue': ttk.Button(
                self.button_frame, 
                text="Continue", 
                command=self.continue_action,
                style='Continue.TButton'
            ),
            'reset': ttk.Button(
                self.button_frame, 
                text="Reset", 
                command=self.reset_action,
                style='Reset.TButton'
            ),
            'exit': ttk.Button(
                self.button_frame, 
                text="Exit", 
                command=root.quit,
                style='Exit.TButton'
            )
        }

        # Pack buttons with more spacing in center frame
        for button in self.buttons.values():
            button.pack(side='left', padx=30)  # Increased padding between buttons

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
            
            # Update counter display instead of label
            self.counter_display.update_count(self.total_stripe_count)

    def process_captured_image(self, image_path):
        # This method can now be simplified since processing is done in counting
        print(f"Image captured at: {image_path}")
        
    def reset_action(self):
        self.total_stripe_count = 0
        self.counter_display.reset()
        messagebox.showinfo("Reset", "Counter has been reset to 0")