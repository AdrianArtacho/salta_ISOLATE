import cv2
import numpy as np
import os



#------------- Browse for the file
import gui.gui_choosefile as gui_choosefile
video_path = gui_choosefile.main(("Select .mp4 file", 'OUTPUT/', (".mp4", ".mov")))

print(video_path)

# file_path = "/path/to/your/file/example.txt"
file_name_splitted, file_extension_splitted = os.path.splitext(video_path)
file_name_without_extension = os.path.basename(file_name_splitted)

print(file_name_without_extension)
print(file_extension_splitted)

# output_video = 'OUTPUT/output_video.mp4'
output_video = 'OUTPUT/'+file_name_without_extension+'_BLACK'+file_extension_splitted

print(output_video)


# Load the video
# video_path = 'input_video.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Prepare output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

# Define the range for light green color in HSV
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask to detect light green color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assuming the largest contour is the light green rectangle
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Create a mask for the rectangle
        rectangle_mask = np.zeros_like(frame)
        cv2.rectangle(rectangle_mask, (x, y), (x+w, y+h), (255, 255, 255), -1)
        
        # Masking everything outside the rectangle
        frame = cv2.bitwise_and(frame, rectangle_mask)
    
    # Write the frame to the output video
    out.write(frame)

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()