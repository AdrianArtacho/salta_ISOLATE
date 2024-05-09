import cv2
import numpy as np

def find_green_square(frame, initial_area=None):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a broader range of green color in HSV
    lower_green = (35, 40, 40)
    upper_green = (75, 255, 255)

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

            # Adjust the area threshold based on the initial detection
            area_threshold = initial_area * 0.5 if initial_area else 100

            # Check for square-like shape and dynamic area (adjust as needed)
            if 0.8 <= aspect_ratio <= 1.2 and area > area_threshold:
                return x, y, x + w, y + h, area

    return None

def crop_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    out = None
    initial_area = None  # To store the area of the green square in the first detection

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Find the green square
        result = find_green_square(frame, initial_area)
        if result:
            x1, y1, x2, y2, area = result
            if initial_area is None:
                initial_area = area  # Set the initial area on first detection
            cropped_frame = frame[y1:y2, x1:x2]

            if out is None and cropped_frame.size != 0:
                height, width, _ = cropped_frame.shape
                out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))

            if cropped_frame.size != 0:
                print(f"Cropping to: {x1}, {y1}, {x2}, {y2}")
                out.write(cropped_frame)
        else:
            print("Green square not found in this frame.")

    cap.release()
    if out:
        out.release()

# Call the function
crop_video('OUTPUT/Bogie3.mp4', 'CROPPED/Bogie3_cropped.mp4')
