import os
import subprocess
import sys

def setup_pwm_permissions():
    if os.geteuid() != 0:
        print("This setup script must be run as root")
        sys.exit(1)
        
    try:
        # Create PWM group
        subprocess.run(['groupadd', '-f', 'pwm'], check=True)
        
        # Add current user to PWM group
        user = os.environ.get('SUDO_USER', os.environ.get('USER'))
        subprocess.run(['usermod', '-aG', 'pwm', user], check=True)
        
        # Create udev rule
        rule_content = 'SUBSYSTEM=="mem", KERNEL=="mem", GROUP="pwm", MODE="0660"\n'
        with open('/etc/udev/rules.d/99-pwm.rules', 'w') as f:
            f.write(rule_content)
            
        # Reload udev rules
        subprocess.run(['udevadm', 'control', '--reload-rules'], check=True)
        subprocess.run(['udevadm', 'trigger'], check=True)
        
        print("PWM permissions setup complete!")
        print("Please log out and log back in for group changes to take effect")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_pwm_permissions()