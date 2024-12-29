from tkinter import ttk
import tkinter as tk
import os
import subprocess
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
        # Create and pack label
        self.label = ttk.Label(
            self.frame,
            text="LED Brightness",
            font=('Helvetica', 30, 'bold')
        )
        self.label.pack(side='top', pady=(0,5))  # Add more padding below label
        
        # Create and pack scale BEFORE value label with more padding
        self.scale = ttk.Scale(
            self.frame,
            from_=0,
            to=100,
            orient='horizontal',
            length=600,
            command=self.on_brightness_change
        )
        self.scale.pack(side='top', pady=(0,5))  # Add padding below scale
        self.scale.set(10)  # Set initial value
    
        # Create and pack value label AFTER scale
        self.value_label = ttk.Label(
            self.frame,
            text="50%",
            font=('Helvetica', 24)
        )
        self.value_label.pack(side='top', pady=(10,10))  # Add padding below value label

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

    def on_brightness_change(self, value):
        try:
            brightness = int(float(value))
            self.value_label.config(text=f"{brightness}%")
            
            # Convert percentage to duty cycle value (0-10000)
            duty = int((brightness / 100.0) * 0x2710)  # 0x2710 = 10000
            self.write_pwm_value(self.PWM_DUTY_ADDR, duty)
        except Exception as e:
            print(f"Error in brightness change: {e}")