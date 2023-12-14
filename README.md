# ISOLATE subject

This script isolates subjects in a video.

---

## USAGE

Activate the virtual environment

```shell
source .venv/bin/activate
```

Run the main script:

```shell
python ISOLATE.py
```

---

## Description

This script is designed for annotating videos using OpenCV. It allows users to draw a rectangle on the video frames and perform various manipulations like resizing and moving the rectangle. This tool is particularly useful for tasks that require frame-by-frame annotation, such as object tracking, video editing, or data labeling for machine learning.

---

## Features

- Draw a resizable and movable rectangle on video frames.
- Ability to pause and resume video processing for detailed editing.
- Shortcuts for quick and easy manipulation of the annotation rectangle.
- Output the annotated video as a new file.

---

## How to Use

1. **Start the Script:** Run the script in your Python environment. Ensure OpenCV is installed.
2. **Pause Immediately:** It's recommended to pause the video as soon as the script starts (by pressing 'p'). This prevents missing the annotation of the first frames.
3. **Draw a Rectangle:** Right-click and drag to draw a rectangle. Release the right-click to set it.
4. **Manipulate the Rectangle:**
   - **Resize:** Use the '+' key (numpad) to increase the size of the rectangle, and the '-' key (numpad) to decrease it. The center of the rectangle remains the same.
   - **Move:** Use the arrow keys to move the rectangle one pixel in the desired direction (up, down, left, right).
5. **Resume Video:** Press 'p' again to resume video processing. The rectangle will be applied to all frames until paused again.
6. **Rewind:** Press 'b' to rewind the video by a few frames if needed.
7. **Quit:** Press 'q' to quit the script. The annotated video will be saved in the specified output directory.

---

## Shortcuts

- **Pause/Resume Video:** 'p' key
- **Enlarge Rectangle:** '+' key (numpad)
- **Shrink Rectangle:** '-' key (numpad)
- **Move Rectangle Up:** Up arrow key
- **Move Rectangle Down:** Down arrow key
- **Move Rectangle Left:** Left arrow key
- **Move Rectangle Right:** Right arrow key
- **Rewind Video:** 'b' key
- **Exit Script:** 'q' key

---

## Output

The annotated video will be saved in a designated output directory with a timestamp in its filename, making it easy to locate and use for further processing or analysis.
