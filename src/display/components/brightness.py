from tkinter import ttk
import tkinter as tk
import os
import mmap
import struct
import grp
import getpass

class BrightnessControl:
    def __init__(self, parent):
        # Check group membership first
        try:
            pwm_group = grp.getgrnam('pwm')
            current_user = getpass.getuser()
            if current_user not in pwm_group.gr_mem:
                raise PermissionError("User must be in the 'pwm' group to control PWM")
        except KeyError:
            raise PermissionError("PWM group not found. Please run setup_pwm.py first")

        # Create frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(side='bottom', pady=30)
        
        # PWM memory addresses
        self.PWM_PERIOD_ADDR = 0xC408002C
        self.PWM_DUTY_ADDR = 0xC4080034

        # Initialize all widgets first before any callbacks
        self._create_widgets()
        
        # Initialize PWM
        self._init_pwm()

    def _create_widgets(self):
        # Create and pack label
        self.label = ttk.Label(
            self.frame,
            text="LED Brightness",
            font=('Helvetica', 30, 'bold')
        )
        self.label.pack(side='top', pady=10)

        # Create and pack value label BEFORE scale
        self.value_label = ttk.Label(
            self.frame,
            text="50%",
            font=('Helvetica', 24)
        )
        self.value_label.pack(side='bottom', pady=5)

        # Create and pack scale
        self.scale = ttk.Scale(
            self.frame,
            from_=0,
            to=100,
            orient='horizontal',
            length=600,
            command=self.on_brightness_change
        )
        self.scale.pack(side='top')
        self.scale.set(50)  # Set initial value

    def _init_pwm(self):
        # Set initial PWM values
        period = 10000
        initial_duty = int(0.5 * period)  # 50% duty cycle
        self.write_pwm_value(self.PWM_PERIOD_ADDR, period)
        self.write_pwm_value(self.PWM_DUTY_ADDR, initial_duty)

    def write_pwm_value(self, address, value):
        """Write value to PWM register through memory mapping"""
        try:
            with open('/dev/mem', 'r+b') as f:
                mem = mmap.mmap(f.fileno(), 4096, offset=address & ~(4096-1))
                packed_value = struct.pack('I', value)
                mem.seek(address & (4096-1))
                mem.write(packed_value)
                mem.close()
        except Exception as e:
            print(f"Error writing to PWM: {e}")
            raise

    def on_brightness_change(self, value):
        try:
            brightness = int(float(value))
            self.value_label.config(text=f"{brightness}%")
            
            period = 10000
            duty = int((brightness / 100.0) * period)
            self.write_pwm_value(self.PWM_DUTY_ADDR, duty)
        except Exception as e:
            print(f"Error in brightness change: {e}")