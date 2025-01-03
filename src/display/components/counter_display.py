from tkinter import ttk
from ..theme import AppTheme

class CounterDisplay:
    def __init__(self, parent):
        # Create a frame to hold the label
        self.frame = ttk.Frame(parent)
        self.frame.pack(side='top', fill='x', pady=(20, 40),padx=(150,0))  # More top padding
        
        self.label = ttk.Label(
            self.frame,
            text="The number of stack sheet: 0",
            style='Counter.TLabel'
        )
        self.label.pack(expand=True)  # Center horizontally
    
    def update_count(self, count):
        """Update the display with new count"""
        self.label.config(text=f"The number of stack sheet: {count}")
    
    def reset(self):
        """Reset the display to zero"""
        self.label.config(text="The number of stack sheet: 0")
