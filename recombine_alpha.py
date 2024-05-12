from moviepy.editor import VideoFileClip, CompositeVideoClip, VideoClip, ImageClip
import numpy as np

def resize_clip(clip, target_width, target_height):
    """Resize a clip to target width and height."""
    return clip.resize(newsize=(target_width, target_height))

def create_mask(frame):
    """Create a mask where black pixels are fully transparent."""
    # Convert frame to grayscale
    gray_frame = np.mean(frame, axis=-1)
    # Create a binary mask where black pixels are fully transparent
    mask = (gray_frame > 10) * 255  # Thresholding to handle variations in black color
    return ImageClip(np.stack([mask] * 3, axis=-1), ismask=True)

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

# Create masks for each clip
mask1 = create_mask(clip1_resized.get_frame(0))
mask2 = create_mask(clip2_resized.get_frame(0))
mask3 = create_mask(clip3_resized.get_frame(0))

# Set the opacity (transparency) for each video
clip1_resized = clip1_resized.set_opacity(0.4)
clip2_resized = clip2_resized.set_opacity(0.4)
clip3_resized = clip3_resized.set_opacity(0.4)

# Overlay the clips with their respective masks
composite_clip = CompositeVideoClip([
    clip1_resized.set_mask(mask1).set_position("center"),
    clip2_resized.set_mask(mask2).set_position("center"),
    clip3_resized.set_mask(mask3).set_position("center")
])

# Write the result to a file
composite_clip.write_videofile("OUTPUT/recombined_alpha.mp4", codec="libx264")
