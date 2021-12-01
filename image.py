import image_slicer
import os
import time
import sound
import threading
import shutil
import webcolors
from colorthief import ColorThief
from picamera import PiCamera
from PIL import UnidentifiedImageError
from math import sqrt

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

def get_image():
    camera = PiCamera()
    camera.resolution = (320, 240)
    for i in enumerate(camera.capture_continuous(os.path.join(pic_path, "img.jpg"), use_video_port=False)):
            time.sleep(4)

# Slicing image from raspberry pi into 2 images from left to right.
def slice():
    try:
        image_slicer.slice(os.path.join(pic_path, "img.jpg"), 2)
    except UnidentifiedImageError:
        time.sleep(.5)
        image_slicer.slice(os.path.join(pic_path, "img.jpg"), 2)
        
    shutil.move(os.path.join(pic_path, "img_01_01.png"), os.path.join(pic_path, "left_half.png"))
    shutil.move(os.path.join(pic_path, "img_01_02.png"), os.path.join(pic_path, "right_half.png"))

Colors = {
    'Black': (0, 0, 0),
    'Gray': (127, 127, 127),
    'Bordeaux': (136, 0, 21),
    'red': (237, 28, 36), 
    'orange': (255, 127, 39),
    'yellow': (255, 242, 0),
    'green': (34, 177, 76),
    'blue': (203, 228, 253),
    'dark blue': (0, 162, 232),
    'purple': (63, 72, 204),
    'white': (255, 255, 255),
    'light gray': (195, 195, 195),
    'light brown': (185, 122, 87),
    'light pink': (255, 174, 201),
    'dark yellow': (255, 201, 14),
    'light yellow': (239, 228, 176),
    'light green': (181, 230, 29),
    'light blue': (153, 217, 234),
    'dark blue': (112, 146, 190),
    'light purple': (200, 191, 231)
}

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in Colors.values():
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    value = min(color_diffs)[1]
    for key in Colors.keys():
        if value == Colors.get(key):
            return key
    return None

# Getting the most dominant color (using k-means clustering) in the 2 images and outputting it as rgb values for both left and right
def get_colors():
    # Slicing the image and setting variables that refrence both the split images
    slice()
    left_rgb = ColorThief(os.path.join(pic_path, "left_half.png")).get_color(quality=1)
    right_rgb = ColorThief(os.path.join(pic_path, "right_half.png")).get_color(quality=1)
    colors = []
    colors.append(closest_color(left_rgb))
    colors.append(closest_color(right_rgb))

    return colors


def loop():
    while True:
        sound.play(get_colors())

t1 = threading.Thread(target=get_image, name='t1')
t2 = threading.Thread(target=loop, name='t2')
t1.start()
t2.start()


