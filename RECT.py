import cv2
import rect_positions

def add_black_rectangle_to_video(input_video_path, output_video_path, positions):
    # Open the video
    video = cv2.VideoCapture(input_video_path)
    
    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Could not open the video file.")
        return

    # Get video properties
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break  # Exit the loop if there are no more frames

        # Get the current time (in seconds)
        current_time = frame_count / fps

        # Move the rectangle based on the time and specified positions
        for position_info in positions:
            start_time, end_time, x, y, w, h = position_info
            if start_time <= current_time < end_time:
                # Add a black rectangle at the specified position
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)
        
        # Write the frame into the output video
        out.write(frame)

        # Increment frame counter
        frame_count += 1

        # Optional: show video in real-time (press 'q' to exit early)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    video.release()
    out.release()
    cv2.destroyAllWindows()



positions = rect_positions.read_rectangles_file('OUTPUT/rectangles_positions.txt')
# exit()
# # Example usage:
# positions = [
#     # (start_time, end_time, x, y, width, height)
#     (0, 136, 0, 0, 600, 950),  # Rectangle from second 0 to 5 at position (100, 100)
#     (136, 142, 0, 0, 200, 950),  # Move to position (300, 200) from second 5 to 10
#     (142, 170, 0, 0, 600, 950),   # Move again to (50, 50) from second 10 to 15
#     (170, 176, 0, 0, 200, 950),
#     (176, 191, 0, 0, 600, 950),
#     (191, 235, 0, 0, 200, 950),
# ]

input_video_path = 'INPUT/LigetiSonate.mp4'  # Path to your input video
output_video_path = 'OUTPUT/output_video_with_rectangles.mp4'  # Path to save the output video

add_black_rectangle_to_video(input_video_path, output_video_path, positions)
