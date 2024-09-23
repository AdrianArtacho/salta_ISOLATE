import cv2

# Global variables for drawing the rectangle
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
current_rectangle = None  # To store the most recent rectangle and its time info
paused = False  # Keep track of the video pause state

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, paused, frame, current_rectangle

    # Only allow drawing when the video is paused
    if paused:
        # When the left mouse button is pressed, record the starting position (ix, iy)
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y

        # When the mouse is moving and drawing is True, show the rectangle dynamically
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                # Copy the original frame and draw on it (for visualization purposes)
                frame_copy = frame.copy()
                cv2.rectangle(frame_copy, (ix, iy), (x, y), (0, 255, 0), 3)  # Green outline, thickness 3
                cv2.imshow('Video', frame_copy)

        # When the left mouse button is released, finalize the rectangle
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            # Save the most recent rectangle (erase the previous one)
            current_rectangle = (ix, iy, x, y, current_time)
            # Redraw the current frame (clear the previous rectangle)
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (ix, iy), (x, y), (0, 255, 0), 3)  # Green outline, thickness 3
            cv2.imshow('Video', frame_copy)

def write_positions_to_file(current_rectangle, filename):
    if current_rectangle is not None:
        ix, iy, x, y, time = current_rectangle
        with open(filename, 'w') as f:
            # Compute width and height
            width = abs(x - ix)
            height = abs(y - iy)
            f.write(f'{time:.2f}, {ix}, {iy}, {width}, {height}\n')
        print(f'Position saved to {filename}')
    else:
        print("No rectangle to save.")

def play_video_and_capture_rectangles(video_path, output_file):
    global frame, current_time, paused, current_rectangle
    video = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    
    if not video.isOpened():
        print("Error: Could not open the video file.")
        return
    
    # Set up the window and mouse callback
    cv2.namedWindow('Video')
    cv2.setMouseCallback('Video', draw_rectangle)

    frame_number = 0

    while video.isOpened():
        if not paused:
            ret, frame = video.read()
            if not ret:
                break  # Exit if the video ends

            # Calculate current time based on frame number and fps
            current_time = frame_number / fps
            frame_number += 1

        # Re-draw the most recent rectangle on the frame if it exists
        if current_rectangle is not None:
            ix, iy, x, y, _ = current_rectangle
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (ix, iy), (x, y), (0, 255, 0), 3)  # Green outline, thickness 3
            cv2.imshow('Video', frame_copy)
        else:
            # If no rectangle, just show the frame
            cv2.imshow('Video', frame)

        key = cv2.waitKey(30) & 0xFF

        # Spacebar to pause/unpause the video
        if key == ord(' '):
            paused = not paused

        # Press 's' to save the most recent rectangle to a file
        if key == ord('s'):
            write_positions_to_file(current_rectangle, output_file)

        # Press 'q' to exit the video
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'INPUT/LigetiSonate.mp4'
output_file = 'OUTPUT/rectangles_positions.txt'

play_video_and_capture_rectangles(video_path, output_file)
