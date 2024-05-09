import cv2
import numpy as np
import os
from datetime import datetime

#------------- Browse for the file
import gui.gui_choosefile as gui_choosefile
filepath = gui_choosefile.main(("Select .mp4 file", '/Volumes/EXTERN/ATLAS\:PHD/TALLIS-MEDIA/isolate/', (".mp4", ".mov")))

print(filepath)
# # exit()
#------------- Kernel Size (cotrols the blur)
kernel_size = 101    ### NEEDS TO BE AN ODD NUMBER!!!!
#-------------

# Initialize global variables
ix, iy, ex, ey = -1, -1, -1, -1
roi_defined = False
drawing = False
paused = False
video_paused = True  # Start with the video paused
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
    # Start drawing the rectangle
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

video_path = filepath
cap = cv2.VideoCapture(video_path)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', draw_rectangle)

# Capture and store the first frame
ret, frame = cap.read()
if ret:
    frame_buffer.append(frame)

# Main loop
while cap.isOpened():
    key = cv2.waitKey(1) & 0xFF
    print("Key pressed:", key)  # Add this line to print out the key code

    if key == ord('+'):
        resize_rectangle(expand=True)
    elif key == ord('-'):
        resize_rectangle(expand=False)
    elif key == ord('p'):
        video_paused = not video_paused
    elif key == ord('q'):
        break
    elif key == 0 or key == 82:  # Up arrow key (Note: 82 is often used in some environments)
        move_rectangle('up')
    elif key == 3 or key == 83:  # Right arrow key
        move_rectangle('right')
    elif key == 2 or key == 81:  # Left arrow key
        move_rectangle('left')
    elif key == 1 or key == 84:  # Down arrow key
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
        # Frame display and manipulation logic here...
        cv2.imshow('Frame', display_frame)

cap.release()
cv2.destroyAllWindows()
