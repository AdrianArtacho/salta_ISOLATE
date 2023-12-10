import cv2
import numpy as np

#-------------
# import gui.gui_choosefile as gui_choosefile
# filepath = gui_choosefile.main(("title", '', '.mp4'))
# print(filepath)
# # exit()
#-------------

def update_roi(frame_number):
    """
    Dummy function to update ROI based on frame number.
    You can replace this with a more sophisticated method or tracking algorithm.
    """
    # Example: Move the ROI 1 pixel to the right every 10 frames
    shift = frame_number // 10
    return 100 + shift, 100, 200, 200  # Update these values as needed

# Load the video
video_path = '/Users/artacho/Downloads/exp5b_RAW.mp4'
cap = cv2.VideoCapture(video_path)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Update ROI based on the frame number
    x, y, w, h = update_roi(frame_number)
    roi = frame[y:y+h, x:x+w]

    # Blur the entire frame
    frame_blurred = cv2.GaussianBlur(frame, (21, 21), 0)

    # Place the unblurred ROI back into the frame
    frame_blurred[y:y+h, x:x+w] = roi

    # Draw a rectangle around the ROI for visualization
    cv2.rectangle(frame_blurred, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Write the frame into the file 'output.mp4'
    out.write(frame_blurred)

    # Display the resulting frame
    cv2.imshow('Frame', frame_blurred)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_number += 1

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()