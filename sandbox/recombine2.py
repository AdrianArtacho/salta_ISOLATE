from moviepy.editor import VideoFileClip, CompositeVideoClip
import numpy as np

def resize_clip(clip, target_width, target_height):
    """Resize a clip to target width and height."""
    return clip.resize(newsize=(target_width, target_height))

def black_to_transparent(frame):
    """Convert black to transparent."""
    # Extract the RGB values
    r, g, b = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
    # Create a mask for black pixels
    mask = (r == 0) & (g == 0) & (b == 0)
    # Create an alpha channel for the frame
    alpha = np.ones_like(r) * 255  # Fully opaque initially
    # Set alpha channel for black pixels to 0
    alpha[mask] = 0
    # Stack RGB channels with alpha channel
    frame_with_alpha = np.dstack((frame, alpha))
    return frame_with_alpha.astype(np.uint8)


# Load your videos
clip1 = VideoFileClip("OUTPUT/exp9f_iso-A_BLACK_resampl1'5.mp4")
clip2 = VideoFileClip("OUTPUT/exp9f_iso-E_BLACK_resampl1'5.mp4")
clip3 = VideoFileClip("OUTPUT/exp9f_iso-J_BLACK_resampl1'5.mp4")

# Determine the size to which all videos will be resized
# For example, resizing every video to the dimensions of the first video
target_width, target_height = clip1.size

# Resize videos
clip1_resized = resize_clip(clip1, target_width, target_height)
clip2_resized = resize_clip(clip2, target_width, target_height)
clip3_resized = resize_clip(clip3, target_width, target_height)

# Apply black to transparent conversion
clip1_resized = clip1_resized.fl_image(black_to_transparent)
clip2_resized = clip2_resized.fl_image(black_to_transparent)
clip3_resized = clip3_resized.fl_image(black_to_transparent)

# Set the opacity (transparency) for each video
clip1_resized = clip1_resized.set_opacity(0.4)
clip2_resized = clip2_resized.set_opacity(0.4)
clip3_resized = clip3_resized.set_opacity(0.4)

# Overlay the clips
composite_clip = CompositeVideoClip([clip1_resized, clip2_resized.set_position("center"), clip3_resized.set_position("center")])

# Write the result to a file
composite_clip.write_videofile("output_video.mp4", codec="libx264")
