import os

def setup_display():
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'