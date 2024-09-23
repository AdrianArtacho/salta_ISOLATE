import cv2

# Global variables for drawing the rectangle
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
current_rectangle = None  # To store the most recent rectangle and its time info
rectangles = []  # To store all drawn rectangles
paused = False  # Keep track of the video pause state

def clear_rectangles_file(filename):
    # Open the file in write mode to clear its contents
    with open(filename, 'w') as f:
        pass  # 'w' mode truncates the file, so we don't need to write anything
    print(f'{filename} has been cleared.')

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
                # Calculate top-left and bottom-right points from (ix, iy) and (x, y)
                x1, y1 = min(ix, x), min(iy, y)  # Top-left corner
                x2, y2 = max(ix, x), max(iy, y)  # Bottom-right corner

                # Copy the original frame and draw on it (for visualization purposes)
                frame_copy = frame.copy()
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Green outline, thickness 3
                cv2.imshow('Video', frame_copy)

        # When the left mouse button is released, finalize the rectangle
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            # Calculate the top-left and bottom-right corners for final rectangle
            x1, y1 = min(ix, x), min(iy, y)
            x2, y2 = max(ix, x), max(iy, y)

            # Save the most recent rectangle and add it to the list of all rectangles
            current_rectangle = (x1, y1, x2, y2, current_time)
            rectangles.append(current_rectangle)

            # Automatically write the rectangle to file
            append_rectangle_to_file(current_rectangle, output_file)

            # Redraw the current frame (clear the previous rectangle)
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Green outline, thickness 3
            cv2.imshow('Video', frame_copy)

def append_rectangle_to_file(rectangle, filename):
    # Append the new rectangle to the file
    with open(filename, 'a') as f:  # 'a' mode opens the file for appending
        x1, y1, x2, y2, time = rectangle
        # Compute width and height
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        # Save top-left corner, width, height, and the timestamp
        f.write(f'{time:.2f}, {x1}, {y1}, {width}, {height}\n')
    print(f'Rectangle added: Top-left ({x1}, {y1}), Width: {width}, Height: {height} at time {time:.2f}s')

def play_video_and_capture_rectangles(video_path, output_file):
    global frame, current_time, paused, current_rectangle, rectangles
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
            x1, y1, x2, y2, _ = current_rectangle
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Green outline, thickness 3
            cv2.imshow('Video', frame_copy)
        else:
            # If no rectangle, just show the frame
            cv2.imshow('Video', frame)

        key = cv2.waitKey(30) & 0xFF

        # Spacebar to pause/unpause the video
        if key == ord(' '):
            paused = not paused

        # Press 'q' to exit the video
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'INPUT/LigetiSonate.mp4'
output_file = 'OUTPUT/rectangles_positions.txt'

clear_rectangles_file(output_file)
play_video_and_capture_rectangles(video_path, output_file)
