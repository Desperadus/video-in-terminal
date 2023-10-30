# ASCII Video Player

## Overview

ASCII Video Player is a Python-based utility that allows you to convert video files into ASCII art, save them as text files, and play them directly within your terminal.

## Dependencies

- Python 3.x
- OpenCV (cv2)
- PIL (Pillow)
- termcolor
- urllib

You can install the required packages via pip:

```bash
pip install opencv-python Pillow termcolor
```

## Usage

### Converting Videos to ASCII Art

```bash
python3 main.py -i <input_file_path> -o <output_file_path> --dims <width>x<height> --frame_rate <frame_rate>
```

- `-i` or `--input`: The input video or image file path.
- `-o` or `--output`: The output ASCII art file path (default is "output.txt").
- `--dims`: Dimensions for the ASCII art (e.g., '100x32'). Default is '100x32'.
- `--frame_rate`: Frame rate for playing ASCII art video (default is 27).
- `--example`: Run an example featuring Big floppa.

### Playing ASCII Videos

```bash
python3 play.py <input_file> [frame_rate]
```

- `<input_file>`: The path of the ASCII video file to be played.
- `[frame_rate]`: Optional frame rate (default is 27).

### Example Usage

```bash
python3 main.py -i example.mp4 -o output.txt --dims 100x32 --frame_rate 27
```

```bash
python3 main.py --example
```

## Contribution

Feel free to open issues or pull requests if you want to contribute to this project.

