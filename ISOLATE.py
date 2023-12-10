import cv2
import numpy as np

# Load the video
video_path = 'path_to_your_video.mp4'
cap = cv2.VideoCapture(video_path)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Define the region of interest (ROI) as [x, y, width, height]
    # You need to update these values based on the position of the dancer
    x, y, w, h = 100, 100, 200, 200
    roi = frame[y:y+h, x:x+w]

    # Blur the entire frame
    frame_blurred = cv2.GaussianBlur(frame, (21, 21), 0)

    # Place the unblurred ROI back into the frame
    frame_blurred[y:y+h, x:x+w] = roi

    # Write the frame into the file 'output.mp4'
    out.write(frame_blurred)

    # Display the resulting frame
    cv2.imshow('Frame', frame_blurred)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
