import cv2
import numpy as np

def find_green_square(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = (40, 40, 40)
    upper_green = (70, 255, 255)

    # Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is found
    if contours:
        # Iterate over all contours to find the best candidate for the green square
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            area = w * h

            # Check for square-like shape and minimum area (adjust as needed)
            if 0.9 <= aspect_ratio <= 1.1 and area > 100:
                return x, y, x + w, y + h

    return None

def crop_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Find the green square
        crop_coordinates = find_green_square(frame)
        if crop_coordinates:
            x1, y1, x2, y2 = crop_coordinates
            cropped_frame = frame[y1:y2, x1:x2]

            if out is None and cropped_frame.size != 0:
                height, width, _ = cropped_frame.shape
                out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))

            if cropped_frame.size != 0:
                out.write(cropped_frame)

    cap.release()
    if out:
        out.release()

# Call the function
crop_video('OUTPUT/Bogie3.mp4', 'CROPPED/Bogie3_cropped.mp4')
