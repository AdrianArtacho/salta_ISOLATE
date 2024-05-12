from moviepy.editor import VideoFileClip

def resample_video(input_path, output_path, target_duration):
    clip = VideoFileClip(input_path)
    current_duration = clip.duration
    if current_duration > target_duration:
        clip = clip.fx.speedx(factor=target_duration / current_duration)
    clip.write_videofile(output_path)
    clip.close()

input_file = "OUTPUT/exp8b (choir solo)_iso_2024-05-12_12-54_BLACK.mp4"
output_file = "OUTPUT/exp8b_resampled.mov"
target_duration = 82  # 1 minute and 22 seconds

resample_video(input_file, output_file, target_duration)
