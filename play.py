from main import play_ascii_video_framerate
import sys

# Check if the user provided at least one argument
if len(sys.argv) < 2:
    print("Usage: python script_name.py <input_file> [frame_rate]")
    sys.exit(1)

# Get the input file path from the first argument
input_file = sys.argv[1]

# Set a default frame rate (e.g., 27) if it's not provided
frame_rate = 27
if len(sys.argv) >= 3:
    frame_rate = int(sys.argv[2])

# Call the function with the provided input file and frame rate
play_ascii_video_framerate(input_file, frame_rate, True)
