#!/bin/bash

# Download the ASCII video file
ascii_video=$(curl -s "https://raw.githubusercontent.com/Desperadus/video-in-terminal/master/shrek.hovno")

# Run the Python code
python3 <<END_PYTHON
import sys
import time

def save_cursor():
    sys.stdout.write("\\033[s")

def hide_cursor():
    sys.stdout.write("\\033[?25l")

def clear_screen():
    sys.stdout.write("\\033[H\\033[2J")

def restore_cursor():
    sys.stdout.write("\\033[u")

def show_cursor():
    sys.stdout.write("\\033[?25h")

def play_ascii_video_framerate(frame_rate=27, loop=True):
    save_cursor()
    hide_cursor()
    clear_screen()
    try:
        frames = '''${ascii_video}'''.split("\\n\\n")
        while True:
            for frame in frames:
                sys.stdout.write(frame)
                time.sleep(1 / frame_rate)
            if not loop:
                break
    except KeyboardInterrupt:
        pass
    finally:
        restore_cursor()
        show_cursor()

play_ascii_video_framerate()
END_PYTHON
