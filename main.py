import cv2
import os
import time
from PIL import Image
from termcolor import colored
import sys
import argparse
import urllib.request


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


def save_floppa_gif():
    file_url = "https://media.tenor.com/RFmgfvXWOsAAAAAd/floppa-big-floppa.gif"
    destination_path = "floppa.gif"
    urllib.request.urlretrieve(file_url, destination_path)
    return destination_path


def save_video_from_url(url):
    file_url = url
    destination_path = "video." + url.split(".")[-1]
    urllib.request.urlretrieve(file_url, destination_path)
    return destination_path


def pixel_to_ascii_color_256(pixel):
    r, g, b = pixel
    ansi_code = 16 + (r // 51) * 36 + (g // 51) * 6 + (b // 51)
    return f"\033[48;5;{ansi_code}m \033[m"


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
    first = True
    while success:
        cv2.imwrite("frame.jpg", image)
        frames.append(
            "[s[?25l" + image_to_ascii_256_optimized2("frame.jpg", width, height)
            if first
            else image_to_ascii_256_optimized2("frame.jpg", width, height)
        )
        success, image = vidcap.read()
    with open(output_path, "w") as output_file:
        output_file.write("\n\n".join(frames))
        os.remove("frame.jpg")


def play_ascii_video_framerate(file_path, frame_rate=27, loop=False):
    save_cursor()
    hide_cursor()
    clear_screen()
    try:
        if loop:
            while True:
                with open(file_path, "r") as file:
                    frames = file.read().split("\n\n")
                    for frame in frames:
                        # os.system("clear")
                        sys.stdout.write(frame)
                        time.sleep(1 / frame_rate)
        with open(file_path, "r") as file:
            frames = file.read().split("\n\n")
            for frame in frames:
                # os.system("clear")
                sys.stdout.write(frame)
                time.sleep(1 / frame_rate)
    except KeyboardInterrupt:
        restore_cursor()
        show_cursor()
    restore_cursor()
    show_cursor()


def image_to_ascii_256_optimized2(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))

    ascii_str = ""  # Initialize terminal
    last_ansi_code = None
    run_length = 0

    for y in range(height):
        if y % height == 0:
            ascii_str += "\033[H"
        for x in range(width):
            pixel = image.getpixel((x, y))
            r, g, b = pixel
            ansi_code = 16 + (r // 51) * 36 + (g // 51) * 6 + (b // 51)
            ascii_char = " "

            if last_ansi_code == ansi_code:
                run_length += 1
            else:
                if run_length > 0:
                    ascii_str += f"{' ' * run_length}"
                ascii_str += f"\033[48;5;{ansi_code}m"
                run_length = 1
                last_ansi_code = ansi_code

        if run_length > 0:
            ascii_str += f"{' ' * run_length}\033[0m"
        run_length = 0
        last_ansi_code = None
        ascii_str += "\n"

    return ascii_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert video to ASCII art and play it in the terminal."
    )
    parser.add_argument(
        "-i", "--input", help="Input video or image file path", default=""
    )
    parser.add_argument(
        "-o", "--output", help="Output ASCII art file path", default="output.txt"
    )
    parser.add_argument(
        "-d",
        "--dims",
        help="Output dimensions (e.g., '100x32')",
        default="100x32",
    )
    parser.add_argument(
        "--frame_rate",
        type=int,
        default=27,
        help="Frame rate for playing ASCII art video (default: 27)",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run example",
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Play video in loop",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default="",
        help="Url to video",
    )
    args = parser.parse_args()

    if args.url != "":
        input_file = save_video_from_url(args.url)
    else:
        input_file = save_floppa_gif() if args.example else args.input
    if input_file == "":
        print(
            "Please provide an input file path: [-i --input] <file_path>. \n Example usage is: python3 main.py -i floppa.gif",
            file=sys.stderr,
        )
        exit(1)
    output_file = args.output
    frame_rate = args.frame_rate

    dimensions = args.dims.split("x")
    width = int(dimensions[0])
    height = int(dimensions[1])

    video_to_ascii_256(input_file, output_file, width, height)
    play_ascii_video_framerate(output_file, frame_rate, args.loop)
