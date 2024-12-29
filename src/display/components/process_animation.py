import tkinter as tk
from tkinter import ttk
import math
import time
from PIL import Image, ImageTk, ImageFilter

class ProcessAnimation:
    def __init__(self, parent):
        self.parent = parent
        self.animation_frame = None
        self.blur_overlay = None
        self.canvas = None
        self.angle = 0
        self.is_running = False
        
    def start(self):
        """Start the processing animation"""
        if self.is_running:
            return
            
        self.is_running = True
        
        # Create blur overlay using Canvas instead of Frame
        self.blur_overlay = tk.Canvas(
            self.parent,
            width=self.parent.winfo_width(),
            height=self.parent.winfo_height(),
            highlightthickness=0
        )
        self.blur_overlay.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create semi-transparent overlay
        self.blur_overlay.create_rectangle(
            0, 0,
            self.parent.winfo_width(),
            self.parent.winfo_height(),
            fill='gray',
            stipple='gray50'  # This creates transparency effect
        )
        
        # Create animation frame with white background
        self.animation_frame = tk.Frame(
            self.blur_overlay,
            bg='white',
            width=200,
            height=200
        )
        self.animation_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create canvas for loading circle
        self.canvas = tk.Canvas(
            self.animation_frame,
            width=100,
            height=100,
            bg='white',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Add "Processing..." text
        self.text = tk.Label(
            self.animation_frame,
            text="Processing...",
            font=('Helvetica', 16, 'bold'),
            bg='white'
        )
        self.text.pack(pady=5)
        
        # Start animation
        self._animate()
        
    def _animate(self):
        """Animate the loading circle"""
        if not self.is_running:
            return
            
        # Clear canvas
        self.canvas.delete('all')
        
        # Draw loading circle
        center = 50
        radius = 20
        start_angle = self.angle
        extent = 300
        
        # Draw arc
        self.canvas.create_arc(
            center-radius, center-radius,
            center+radius, center+radius,
            start=start_angle, extent=extent,
            style='arc', width=4
        )
        
        # Update angle
        self.angle = (self.angle + 10) % 360
        
        # Schedule next animation frame
        if self.is_running:
            self.parent.after(50, self._animate)
        
    def stop(self):
        """Stop the processing animation"""
        self.is_running = False
        
        if self.blur_overlay:
            self.blur_overlay.destroy()
            self.blur_overlay = None
            
        if self.animation_frame:
            self.animation_frame.destroy()
            self.animation_frame = None
            
        self.canvas = None
