import cv2
import numpy as np
import os
from datetime import datetime

# Initialize global variables
ix, iy, ex, ey = -1, -1, -1, -1
roi_defined = False
drawing = False
paused = False
frame_buffer = []
frame_number = 0
max_buffer_size = 100  # Adjust buffer size as needed

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, ex, ey, roi_defined, drawing

    if event == cv2.EVENT_RBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        ex, ey = x, y
        roi_defined = False

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        ex, ey = x, y

    elif event == cv2.EVENT_RBUTTONUP:
        drawing = False
        ex, ey = x, y
        roi_defined = True

    elif event == cv2.EVENT_LBUTTONDOWN and roi_defined:
        w, h = ex - ix, ey - iy
        ix, iy = x - w // 2, y - h // 2
        ex, ey = ix + w, iy + h

# Function to rewind and adjust the frame buffer
def rewind_frames(steps):
    global frame_number, frame_buffer, paused
    if frame_number > steps:
        frame_number = max(0, frame_number - steps)
        del frame_buffer[-steps:]  # Remove the last 'steps' frames
        paused = True  # Pause after rewinding

# Load the video
video_path = '/Users/artacho/Downloads/exp5b_RAW.mp4'
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
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break
        if len(frame_buffer) >= max_buffer_size:
            frame_buffer.pop(0)
        frame_buffer.append(frame)
        frame_number += 1

    display_frame = frame_buffer[-1].copy()

    if roi_defined and ix != -1 and iy != -1 and ex != -1 and ey != -1:
        mask = np.zeros(display_frame.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (ix, iy), (ex, ey), 255, -1)
        masked_frame = cv2.bitwise_and(display_frame, display_frame, mask=mask)
        blurred_frame = cv2.GaussianBlur(display_frame, (51, 51), 0)
        outside_roi = cv2.bitwise_and(blurred_frame, blurred_frame, mask=cv2.bitwise_not(mask))
        display_frame = cv2.add(masked_frame, outside_roi)
        if not drawing:
            cv2.rectangle(display_frame, (ix, iy), (ex, ey), (0, 255, 0), 2)
        else:
            cv2.rectangle(display_frame, (ix, iy), (ex, ey), (0, 255, 0), 2, cv2.LINE_AA)  # Dashed rectangle

    cv2.imshow('Frame', display_frame)

    out.write(display_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        paused = not paused
    elif key in [ord('b'), ord('n'), ord('m')]:
        steps = 1 if key == ord('b') else 10 if key == ord('n') else 100
        rewind_frames(steps)

cap.release()
out.release()
cv2.destroyAllWindows()
