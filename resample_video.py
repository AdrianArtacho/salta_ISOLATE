"""
This script takes in a video and modifies the speed to match a desired length in seconds.
Additionally, it can resize the image...
"""

from moviepy.editor import *
import time as tt
import gui.gui_enterstring as gui_enterstring
import gui.gui_choosefile as gui_choosefile
import os


def resample(fpath, directory, output_filename, extension):
    # fpath =  "OUTPUT/exp8b (choir solo)_iso_2024-05-12_12-54_BLACK.mp4"
    clip = VideoFileClip(fpath)
    print('clip.size: ', clip.size)
    # [720, 720]

    # exit()
    current_duration = clip.duration

    print("Duration of video : ", current_duration)
    print("FPS : ", clip.reader.fps)


    returned_string = gui_enterstring.main("current length:   "+str(current_duration)+" (seconds)", 
                                        "desired length:", 
                                        "Set desired length", 
                                        font = ("Arial", 16), 
                                        default_text=clip.duration,
                                        verbose=False)


    desired_duration = float(returned_string)
    print("returned_string", returned_string)

    factor_mul = current_duration / desired_duration

    print("factor_mul", factor_mul)

    # exit()
    # clip1 = clip.speedx(factor_mul).resize([1920, 1080])
    clip1 = clip.speedx(factor_mul)
    # exit()
    print('clip1.size: ', clip.size)
    # [1920, 1080]
    # exit()
    print("Duration of clip1 : ", clip1.duration)
    print("FPS clip1 : ", clip1.reader.fps)
    # exit()

    string_with_point = str(factor_mul)
    string_with_apostrophe = string_with_point.replace(".", "'")
    
    tmp_mp4 = directory+'/'+output_filename+string_with_apostrophe+'.mp4'        # temporary file

    # exit()
    clip1.write_videofile(tmp_mp4)
    # tt.sleep(0.5)
    # os.system('explorer ' + tmp_mp4)    # open the file: tmp_mp4.

def main(fpath='', verbose=False):
    if fpath == '':
        print("need to browse")
        
        fpath = gui_choosefile.main(("Select .mp4 file",
                                     'OUTPUT/',
                                     (".mp4", ".mov")))

    else:
        fpath = fpath
    
    if verbose:
        print("fpath:", fpath)
    
    # Split the file path into directory and filename
    directory, full_filename = os.path.split(fpath)
    # Split the filename into name and extension
    filename, extension = os.path.splitext(full_filename)

    output_filename = filename+"_resampl"

    if verbose:
        print("directory", directory)
        print("output_filename", output_filename)

    # exit()
    resample(fpath, directory, output_filename, extension)


if __name__ == "__main__":
    # main(fpath = "OUTPUT/exp8b (choir solo)_iso_2024-05-12_12-54_BLACK.mp4")
    main(verbose=True)
