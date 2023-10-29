import cv2
import time
from PIL import Image
from termcolor import colored


def pixel_to_ascii_color_256(pixel):
    ascii_chars = "@%#*+=-:. "
    r, g, b = pixel
    # Convert RGB to ANSI 256-color code
    ansi_code = 16 + (r // 51) * 36 + (g // 51) * 6 + (b // 51)
    brightness = int((r + g + b) / 3)
    ascii_char = ascii_chars[int(brightness / 32)]
    ascii_char = " "
    return f"\033[48;5;{ansi_code}m{ascii_char}\033[m"


def image_to_ascii_256(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    ascii_str = ""
    for y in range(height):
        for x in range(width):
            ascii_str += pixel_to_ascii_color_256(image.getpixel((x, y)))
        ascii_str += "\n"
    return ascii_str


# Function to extract frames from video and convert them to colored ASCII


def video_to_ascii_256(video_path, output_path, width, height):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    frames = []
    while success:
        cv2.imwrite("frame.jpg", image)
        frames.append(image_to_ascii_256("frame.jpg", width, height))
        success, image = vidcap.read()
    with open(output_path, "w") as output_file:
        output_file.write("\n\n".join(frames))


# Function to play ASCII video in terminal with frame rate control


def play_ascii_video_framerate(file_path, frame_rate=1):
    with open(file_path, "r") as file:
        # Assume each frame is separated by two newlines
        frames = file.read().split("\n\n")
        for frame in frames:
            print(frame)
            time.sleep(1 / frame_rate)


# Convert video to colored ASCII
video_to_ascii_256("floppa-ears.gif", "output.txt", 100, 40)

# Play colored ASCII video in terminal at 1 FPS
play_ascii_video_framerate("output.txt", frame_rate=10)
