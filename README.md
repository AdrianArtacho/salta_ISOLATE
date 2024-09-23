# ISOLATE subject

This script isolates subjects in a video.

---

## INSTALL

Create a venv and install required dependencies:

```bash
python3 -m venv ./.venv

#activate venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## USAGE (Black our area)

Activate venv and run `rect_HELPER.py` to set the position of the black rectangle.

```bash
source .venv/bin/activate
python rect_HELPER.py
```

You may draw rectangles on the video image, only when paused (`spacebar`).
The position of said rectangles will be stored as `OUTPUT/rectangle_positions.txt`.

Now run the main script, which will use `rectangle_positions.txt` to render the video with a black rectangle covering those areas. The result will be saved as `OUTPUT/output_video_with_rectangles.mp4`.

```bash
python RECT.py
```

---

## USAGE (focus on area)

Activate the virtual environment and run the main script:

```bash
source .venv/bin/activate
python ISOLATE.py
```

To 'blacken' all image but that inside the green square, run this script on the *already isolated* video:

```shell
python blacken.py
```

Both `_iso.mp4` and `_iso_black.mp4` files will be saved onto the `/OUTPUT` folder.

The produced videos seem to have a reduced speed. In order to resample them to their original speed, run:

```shell
python resample_video.py
```

You will be asked to set the desired lenght (in seconds) for the video. Check out the original footage for this.

Finally, you may want to recombine the isolated videos into one. This can be done in two ways:

1. Simply apply transparecy to all videos and overlay them on top of each other.

   ```bash
   python recombine_trans.py
   ```

2. Or create a mask where black pixels are fully transparent (specially useful for *blackened* isolated videos). And then combine them.

   ```shell
   python recombine_alpha.py
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

### Blacken

Blacken outside of rectangle

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

---

## Key detection

If your mappings are different, feel free to run the little key detection script, to see what they are.

```python
cd pyt/input
python Key_detection.py
```
