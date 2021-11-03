import image_slicer
import os
import shutil

# Setting Dirsectory for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

# Slicing image from raspberry pi into 2 images form left and right.
def slice():
    image_slicer.slice(os.path.join(pic_path, "download.png"), 2)
    shutil.move(os.path.join(pic_path, "download_01_01.png"), os.path.join(pic_path, "first_half.png"))
    shutil.move(os.path.join(pic_path, "download_01_02.png"), os.path.join(pic_path, "second_half.png"))
slice()