import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os
import threading
import queue
import time

class CameraFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=30)
        
        # Initialize camera with optimized settings
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")
            
        # Optimize camera settings for performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)  # Increased buffer
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Use MJPG format
        
        # Add brightness and contrast settings
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)  # Default is usually 100, increase for brighter image
        self.cap.set(cv2.CAP_PROP_CONTRAST, 128)    # Default is usually 128
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Enable auto-exposure
        
        # Create canvas for video display
        self.canvas = tk.Canvas(
            self.frame,
            width=800,
            height=600,
            bg='black',
            highlightthickness=2,
            highlightbackground="gray"
        )
        self.canvas.pack(pady=10)
        
        # Create frame queue with larger buffer
        self.frame_queue = queue.Queue(maxsize=4)
        
        # Create output directory
        os.makedirs("captured_images", exist_ok=True)
        
        # Performance monitoring
        self.last_time = time.time()
        self.frame_count = 0
        self.fps = 0
        
        # Start frame capture thread
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        # Start display update
        self.update_display()
    
    def capture_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Add gamma correction if needed
                gamma = 1.2  # Adjust this value: >1 makes image brighter, <1 makes it darker
                frame = cv2.pow(frame / 255.0, gamma) * 255.0
                frame = frame.astype('uint8')
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                try:
                    self.frame_queue.put_nowait(frame_rgb)
                except queue.Full:
                    try:
                        self.frame_queue.get_nowait()
                        self.frame_queue.put_nowait(frame_rgb)
                    except queue.Empty:
                        pass
            
            # Add a small sleep to prevent thread from consuming too much CPU
            time.sleep(0.001)
    
    def update_display(self):
        try:
            frame_rgb = self.frame_queue.get_nowait()
            
            # Calculate FPS
            self.frame_count += 1
            current_time = time.time()
            if current_time - self.last_time >= 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_time = current_time
            
            # Optimize image conversion
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update canvas efficiently
            self.canvas.delete("all")
            self.canvas.create_image(400, 300, image=imgtk)
            self.canvas.imgtk = imgtk
            
            # Display FPS
            self.canvas.create_text(50, 20, text=f"FPS: {self.fps}", fill="white")
            
        except queue.Empty:
            pass
        
        # Schedule next update with minimal delay
        self.frame.after(8, self.update_display)  # Reduced to 8ms (~120 Hz refresh rate)
    
    def capture_image(self):
        try:
            frame_rgb = self.frame_queue.get_nowait()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captured_images/image_{timestamp}.jpg"
            
            # crop_frame = crop_main_frame(frame_rgb)   
            # convert_to_64x384(crop_frame)

            # Convert RGB back to BGR for saving
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, frame_bgr)
            return filename
        except queue.Empty:
            return None

    def crop_main_frame(self):
        # crop the main stacked sheet image 
        pass  
    
    def convert_to_64x384 (self) : 
        pass  
            
    def set_count_callback(self, callback):
        self.count_callback = callback
        
    def release(self):
        self.running = False
        if self.capture_thread.is_alive():
            self.capture_thread.join()
        if self.cap.isOpened():
            self.cap.release()
    
    def __del__(self):
        self.release()