import cv2
import numpy as np
import os
from datetime import datetime

# Initialize global variables
ix, iy, ex, ey = -1, -1, -1, -1
roi_defined = False
drawing = False
paused = False
video_paused = False  # Flag for pausing video capture and recording
frame_buffer = []
frame_number = 0
max_buffer_size = 30

# Function to resize the rectangle
def resize_rectangle(expand=True):
    global ix, iy, ex, ey
    if roi_defined:
        center_x, center_y = (ix + ex) // 2, (iy + ey) // 2
        width, height = ex - ix, ey - iy
        width += 4 if expand else -4
        height += 4 if expand else -4
        ix, iy = center_x - width // 2, center_y - height // 2
        ex, ey = center_x + width // 2, center_y + height // 2

# Function to move the rectangle
def move_rectangle(direction):
    global ix, iy, ex, ey
    moving_rectangle_pixels = 3
    if roi_defined:
        if direction == 'up':
            iy -= moving_rectangle_pixels
            ey -= moving_rectangle_pixels
        elif direction == 'down':
            iy += moving_rectangle_pixels
            ey += moving_rectangle_pixels
        elif direction == 'left':
            ix -= moving_rectangle_pixels
            ex -= moving_rectangle_pixels
        elif direction == 'right':
            ix += moving_rectangle_pixels
            ex += moving_rectangle_pixels

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, ex, ey, roi_defined, drawing, paused
    # ... existing code ...

    if event == cv2.EVENT_RBUTTONDOWN:
        drawing = True
        paused = True
        ix, iy = x, y
        ex, ey = x, y
        roi_defined = False

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        ex, ey = x, y

    elif event == cv2.EVENT_RBUTTONUP:
        drawing = False
        paused = False
        ex, ey = x, y
        roi_defined = True

    elif event == cv2.EVENT_LBUTTONDOWN and roi_defined:
        w, h = ex - ix, ey - iy
        ix, iy = x - w // 2, y - h // 2
        ex, ey = ix + w, iy + h

# Load the video
# video_path = '/Users/artacho/Downloads/exp5b_RAW.mp4'
video_path = '/Volumes/EXTERN/TALLIS-MEDIA/isolate/shorty.mov'
cap = cv2.VideoCapture(video_path)

# Create output directory if it doesn't exist
output_dir = 'OUTPUT'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create output video filename with timestamp and source reference
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
base_name = os.path.basename(video_path).split('.')[0]
output_filename = f'{output_dir}/{base_name}_iso_{timestamp}.mp4'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(output_filename, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', draw_rectangle)

while cap.isOpened():
    key = cv2.waitKey(1) & 0xFF

    # Handle key events for resizing and moving
    if key == ord('+'):  # Numpad '+' to expand rectangle
        resize_rectangle(expand=True)
    elif key == ord('-'):  # Numpad '-' to shrink rectangle
        resize_rectangle(expand=False)
    elif key == ord('p'):
        video_paused = not video_paused
    elif key == 0:  # Up arrow key 82
        move_rectangle('up')
    elif key == 3:  # Right arrow key 83
        move_rectangle('right')
    elif key == 2:  # Left arrow key 81
        move_rectangle('left')
    elif key == 1:  # Down arrow key 84
        move_rectangle('down')

    if not video_paused:
        ret, frame = cap.read()
        if not ret:
            break
        frame_buffer.append(frame)
        if len(frame_buffer) > max_buffer_size:
            frame_buffer.pop(0)
        frame_number += 1

    display_frame = frame_buffer[-1].copy() if frame_buffer else None

    if display_frame is not None:
        if roi_defined and ix != -1 and iy != -1 and ex != -1 and ey != -1:
            mask = np.zeros(display_frame.shape[:2], dtype="uint8")
            cv2.rectangle(mask, (ix, iy), (ex, ey), 255, -1)
            masked_frame = cv2.bitwise_and(display_frame, display_frame, mask=mask)
            blurred_frame = cv2.GaussianBlur(display_frame, (51, 51), 0)
            outside_roi = cv2.bitwise_and(blurred_frame, blurred_frame, mask=cv2.bitwise_not(mask))
            display_frame = cv2.add(masked_frame, outside_roi)
            cv2.rectangle(display_frame, (ix, iy), (ex, ey), (0, 255, 0), 2)

        cv2.imshow('Frame', display_frame)

    if not video_paused and not paused:
        out.write(display_frame)

    if key == ord('q'):
        break
    elif key == ord('b') and frame_number > max_buffer_size:
        frame_buffer.pop()  # Remove the current frame
        frame_number -= 2  # Go back one frame
        paused = True

cap.release()
out.release()
cv2.destroyAllWindows()
