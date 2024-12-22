import tkinter as tk
from tkinter import ttk
import os
from .components.camera import CameraFrame
from .components.buttons import ButtonFrame
from .components.title import TitleLabel
from .utils.config import setup_display
from .components.brightness import BrightnessControl


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Counting Machine")
        
        # Make it fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.resizable(True, True)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        # Add components
        self.title = TitleLabel(self.main_frame)
        self.camera = CameraFrame(self.main_frame)
        self.buttons = ButtonFrame(self.main_frame, self.root,self.camera)          
        self.brightness = BrightnessControl(self.main_frame)

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