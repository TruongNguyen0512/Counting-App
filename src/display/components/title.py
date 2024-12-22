from tkinter import ttk

class TitleLabel:
    def __init__(self, parent):
        # Make title bigger
        self.label = ttk.Label(
            parent,
            text="Counting Machine",
            font=('Helvetica', 50, 'bold')
        )
        self.label.pack(pady=30)