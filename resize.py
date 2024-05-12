from moviepy.editor import *
import time as tt

# your fpath
fpath =  "OUTPUT/exp8b (choir solo)_iso_2024-05-12_12-54_BLACK.mp4"
clip = VideoFileClip(fpath)
print('clip.size: ', clip.size)
# [720, 720]

print("Duration of video : ", clip.duration)
print("Duration of video : ", clip.reader.fps)

clip1 = clip.speedx(0.5).resize([1920, 1080])
print('clip1.size: ', clip.size)
# [1920, 1080]
print("Duration of clip1 : ", clip1.duration)
print("Duration of clip1 : ", clip1.reader.fps)


tmp_mp4 = '__temp__.mp4'        # temporary file

clip1.write_videofile(tmp_mp4)
tt.sleep(0.5)
os.system('explorer ' + tmp_mp4)    # open the file: tmp_mp4.