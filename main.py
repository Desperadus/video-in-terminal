import cv2
import os
import time
from PIL import Image
from termcolor import colored
import sys
import argparse


def save_cursor():
    sys.stdout.write("\x1b[s")


def restore_cursor():
    sys.stdout.write("\x1b[u")


def hide_cursor():
    sys.stdout.write("\x1b[?25l")


def show_cursor():
    sys.stdout.write("\x1b[?25h")


def clear_screen():
    sys.stdout.write("\x1b[2J")
    sys.stdout.write("\x1b[H")


def pixel_to_ascii_color_256(pixel):
    ascii_chars = "@%#*+=-:. "
    r, g, b = pixel
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
        os.remove("frame.jpg")


def play_ascii_video_framerate(file_path, frame_rate=1):
    save_cursor()
    hide_cursor()
    clear_screen()
    try:
        with open(file_path, "r") as file:
            frames = file.read().split("\n\n")
            for frame in frames:
                os.system("clear")
                print(frame, end="")
                time.sleep(1 / frame_rate)
    except KeyboardInterrupt:
        restore_cursor()
        show_cursor()
    restore_cursor()
    show_cursor()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert video to ASCII art and play it in the terminal."
    )
    parser.add_argument(
        "-i", "--input", help="Input video or image file path", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Output ASCII art file path", default="ouput.txt"
    )
    parser.add_argument(
        "-d",
        "--dimensions",
        help="Output dimensions (e.g., '100x32')",
        default="100x32",
    )
    parser.add_argument(
        "--frame_rate",
        type=int,
        default=27,
        help="Frame rate for playing ASCII art video (default: 27)",
    )

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    frame_rate = args.frame_rate

    dimensions = args.dimensions.split("x")
    width = int(dimensions[0])
    height = int(dimensions[1])

    video_to_ascii_256(input_file, output_file, width, height)
    play_ascii_video_framerate(output_file, frame_rate)
