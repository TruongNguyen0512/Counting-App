import tkinter as tk
from tkinter import ttk
import os
from .components.camera import CameraFrame
from .components.buttons import ButtonFrame
from .components.title import TitleLabel
from .utils.config import setup_display
from .components.brightness import BrightnessControl
from .components.process_animation import ProcessAnimation
from .theme import AppTheme


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Sheet Counter")
        
        # Configure window
        self.root.configure(bg=AppTheme.LIGHT_GRAY)
        
        # Make it fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.resizable(True, True)
        
        # Create main frame with themed background
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')
        self.main_frame.configure(style='Main.TFrame')

        # Initialize process animation first
        self.process_animation = ProcessAnimation(self.main_frame)

        # Configure styles
        style = ttk.Style()
        AppTheme.configure_styles(style)
        
        # Initialize components in correct order
        self.title = TitleLabel(self.main_frame)
        self.brightness = BrightnessControl(self.main_frame)  # Initialize before camera
        self.camera = CameraFrame(self.main_frame)
        self.buttons = ButtonFrame(
            self.main_frame, 
            self.root, 
            self.camera, 
            self.process_animation
        )

        # Print frame size after all components are initialized
        self.main_frame.update()  # Ensure geometry is updated
        width = self.main_frame.winfo_width()
        height = self.main_frame.winfo_height()
        print(f"Main frame size: {width}x{height}")
        print(f"Main frame geometry: {self.main_frame.winfo_geometry()}")

        # Bind keys
        self.setup_key_bindings()
        
        self.is_fullscreen = True

    def setup_key_bindings(self):
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)