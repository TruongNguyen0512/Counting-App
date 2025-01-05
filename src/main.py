#!/usr/bin/env python3
import tkinter as tk
from display.app import DesktopApp
from display.utils.config import setup_display
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app
        self.last_reload = time.time()
        
    def on_modified(self, event):
        # Ignore non-python files
        if not event.src_path.endswith('.py'):
            return
            
        # Prevent multiple reloads within 1 second
        if time.time() - self.last_reload < 1:
            return
            
        print(f"\nCode change detected in {event.src_path}")
        print("Reloading application...")
        self.last_reload = time.time()
        
        # Destroy current window
        self.app.root.destroy()
        
        # Restart the application
        os.execv(sys.executable, ['python'] + sys.argv)

def main():
    setup_display()
    try:
        root = tk.Tk()
        app = DesktopApp(root)
        
        # Set up file watcher
        event_handler = CodeChangeHandler(app)
        observer = Observer()
        observer.schedule(
            event_handler, 
            path=os.path.dirname(os.path.abspath(__file__)), 
            recursive=True
        )
        observer.start()
        
        try:
            root.mainloop()
        finally:
            observer.stop()
            observer.join()
            
    except tk.TclError as e:
        print(f"Error: Could not connect to display. Make sure X server is running.\n{e}")
        exit(1)

if __name__ == "__main__":
    main()