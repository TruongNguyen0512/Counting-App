from tkinter import ttk
import tkinter as tk
import os
import subprocess
import grp
import getpass 
from ..theme import AppTheme

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

        # Create frame with explicit styling
        self.frame = ttk.Frame(parent, style='Brightness.TFrame')
        self.frame.pack(side='right', fill='y', padx=30, pady=30)  # Removed before parameter
        
        # Update PWM memory addresses to match working configuration
        self.PWM_CTRL_ADDR = 0xC40000D0
        self.PWM_CLOCK_ADDR = 0xC4080108
        self.PWM_PERIOD_ADDR = 0xC408002C
        self.PWM_CTRL2_ADDR = 0xC4080030
        self.PWM_DUTY_ADDR = 0xC4080034
        self.PWM_HELPER = os.path.join(os.path.dirname(__file__), '../../pwm_helper/pwm_control')

        # Initialize all widgets first before any callbacks
        self._create_widgets()
        
        # Initialize PWM
        self._init_pwm()

    def _create_widgets(self):
        # Create and pack label with explicit styling
        self.label = ttk.Label(
            self.frame,
            text="Brightness",
            style='Brightness.TLabel'
        )
        self.label.pack(side='top', pady=(10, 10))
        
        # Create scale with explicit styling and border
        self.scale = ttk.Scale(
            self.frame,
            from_=100,
            to=0,
            orient='vertical',
            length=400,
            style='Brightness.Vertical.TScale'
        )
        self.scale.configure(command=self.update_brightness)
        self.scale.set(50)
        self.scale.pack(side='top', pady=10, ipadx=10, ipady=0)

    def _init_pwm(self):
        """Initialize PWM with the same sequence as test.sh"""
        try:
            # Initialize PWM control registers
            self.write_pwm_value(self.PWM_CTRL_ADDR, 0x0)    # Disable PWM
            self.write_pwm_value(self.PWM_CLOCK_ADDR, 0x7D0) # Set clock
            self.write_pwm_value(self.PWM_PERIOD_ADDR, 0x2710) # Set period to 10000
            self.write_pwm_value(self.PWM_CTRL2_ADDR, 0x0)   # Clear control register
            
            # Set initial duty cycle (50%)
            initial_duty = 0x1388  # 5000 (50% of 10000)
            self.write_pwm_value(self.PWM_DUTY_ADDR, initial_duty)
            
        except Exception as e:
            print(f"Error initializing PWM: {e}")
            raise

    def write_pwm_value(self, address, value):
        """Write value to PWM register using helper program"""
        try:
            result = subprocess.run(
                [self.PWM_HELPER, hex(address), hex(value)],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip() != "OK":
                raise ValueError(f"PWM write failed: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error writing to PWM: {e}")
            raise

    def update_brightness(self, value):
        """Update brightness value"""
        try:
            brightness = int(float(value))
            print(f"Brightness set to: {brightness}")
            
            # Convert percentage to duty cycle value (0-10000)
            duty = int((brightness / 100.0) * 0x2710)  # 0x2710 = 10000
            self.write_pwm_value(self.PWM_DUTY_ADDR, duty)
        except Exception as e:
            print(f"Error in brightness change: {e}")