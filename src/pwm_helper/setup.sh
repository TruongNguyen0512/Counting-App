#!/bin/bash

# Compile the helper program
gcc -o pwm_control pwm_control.c

# Set ownership and permissions
sudo chown root:pwm pwm_control
sudo chmod u+s,g+x pwm_control

# Verify setup
ls -l pwm_control
