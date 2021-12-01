import image_slicer
import os
import time
import sound
import threading
import shutil
import webcolors
from colorthief import ColorThief
from picamera import PiCamera

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

def get_image():
    camera = PiCamera()
    camera.resolution = (352, 240)
    for i, filename in enumerate(camera.capture_continuous(os.path.join(pic_path, "img.jpg"), use_video_port=False)):
            print(filename)
            time.sleep(1)

# Slicing image from raspberry pi into 2 images from left to right.
def slice():
    image_slicer.slice(os.path.join(pic_path, "img.jpg"), 2)
    shutil.move(os.path.join(pic_path, "img_01_01.png"), os.path.join(pic_path, "left_half.png"))
    shutil.move(os.path.join(pic_path, "img_01_02.png"), os.path.join(pic_path, "right_half.png"))

  
# Getting the most dominant color (using k-means clustering) in the 2 images and outputting it as rgb values for both left and right
def get_colors():
    print("test\n")
    # Slicing the image and setting variables that refrence both the split images
    slice()
    left_rgb = ColorThief(os.path.join(pic_path, "left_half.png")).get_color(quality=1)
    right_rgb = ColorThief(os.path.join(pic_path, "right_half.png")).get_color(quality=1)
    colors = []
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - left_rgb[0]) ** 2
        gd = (g_c - left_rgb[1]) ** 2
        bd = (b_c - left_rgb[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    colors.append(min_colours[min(min_colours.keys())])
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - right_rgb[0]) ** 2
        gd = (g_c - right_rgb[1]) ** 2
        bd = (b_c - right_rgb[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    colors.append(min_colours[min(min_colours.keys())])

    return colors

get_image()
# t1 = threading.Thread(target=get_image, name='t1')
# t1.start()
# while True:
#     t2 = threading.Thread(target=sound.play(get_colors()), name='t2')
#     t2.start()
