import cv2

# Global variables for drawing the rectangle
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
rectangles = []  # To store the drawn rectangles with time info
paused = False  # Keep track of the video pause state

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, paused, frame

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
                cv2.rectangle(frame_copy, (ix, iy), (x, y), (0, 0, 0), 2)
                cv2.imshow('Video', frame_copy)

        # When the left mouse button is released, finalize the rectangle
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            # Save the rectangle coordinates and the time (frame number)
            rectangles.append((ix, iy, x, y, current_time))
            cv2.rectangle(frame, (ix, iy), (x, y), (0, 0, 0), 2)
            cv2.imshow('Video', frame)

def write_positions_to_file(rectangles, filename):
    with open(filename, 'w') as f:
        for rect in rectangles:
            ix, iy, x, y, time = rect
            # Compute width and height
            width = abs(x - ix)
            height = abs(y - iy)
            f.write(f'{time:.2f}, {ix}, {iy}, {width}, {height}\n')
    print(f'Positions saved to {filename}')

def play_video_and_capture_rectangles(video_path, output_file):
    global frame, current_time, paused
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

        # Display the frame
        cv2.imshow('Video', frame)

        key = cv2.waitKey(30) & 0xFF

        # Spacebar to pause/unpause the video
        if key == ord(' '):
            paused = not paused

        # Press 's' to save the positions to a file
        if key == ord('s'):
            write_positions_to_file(rectangles, output_file)

        # Press 'q' to exit the video
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# Example usage
video_path = 'INPUT/LigetiSonate.mp4'
output_file = 'OUTPUT/rectangles_positions.txt'

play_video_and_capture_rectangles(video_path, output_file)
