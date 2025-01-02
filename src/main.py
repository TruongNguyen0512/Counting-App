#!/usr/bin/env python3
import tkinter as tk
from display.app import DesktopApp
from display.utils.config import setup_display

def main():
    setup_display()
    try:
        root = tk.Tk()
        app = DesktopApp(root)
        root.mainloop()
    except tk.TclError as e:
        print(f"Error: Could not connect to display. Make sure X server is running.\n{e}")
        exit(1)

if __name__ == "__main__":
    main()