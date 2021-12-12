import image_slicer
import os
import time
import sound
import threading
import shutil
from PIL import Image
from PIL import UnidentifiedImageError
from math import sqrt
from picamera import PiCamera

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

def get_image():
    camera = PiCamera()
    camera.resolution = (320, 240)
    for i in enumerate(camera.capture_continuous(os.path.join(pic_path, "img.jpg"), use_video_port=False)):
            time.sleep(2)

# Slicing image from raspberry pi into 2 images from left to right.
def slice():
    try:
        image_slicer.slice(os.path.join(pic_path, "img.png"), 2)
    except UnidentifiedImageError:
        time.sleep(.25)
        image_slicer.slice(os.path.join(pic_path, "img.png"), 2)
        
    shutil.move(os.path.join(pic_path, "img_01_01.png"), os.path.join(pic_path, "left_half.png"))
    shutil.move(os.path.join(pic_path, "img_01_02.png"), os.path.join(pic_path, "right_half.png"))

Colors = {
    'black': (0, 0, 0),
    'gray': (127, 127, 127),
    'bordeaux': (136, 0, 21),
    'red': (237, 28, 36), 
    'orange': (255, 127, 39),
    'yellow': (255, 242, 0),
    'green': (34, 177, 76),
    'blue': (203, 228, 253),
    'dark_blue': (0, 162, 232),
    'purple': (63, 72, 204),
    'white': (255, 255, 255),
    'light_gray': (195, 195, 195),
    'light_brown': (185, 122, 87),
    'light_pink': (255, 174, 201),
    'dark_yellow': (255, 201, 14),
    'light_yellow': (239, 228, 176),
    'light_green': (181, 230, 29),
    'light_blue': (153, 217, 234),
    'dark_blue': (112, 146, 190),
    'light_purple': (200, 191, 231)
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

# Getting the most dominant color in the 2 images and outputting it as rgb values for both left and right
def get_colors():
    # Slicing the image and setting variables that refrence both the split images
    slice()

    colors = []
    with Image.open(os.path.join(pic_path, "left_half.png")) as img:
        img.thumbnail((100, 100))
        # Reduce colors (uses k-means internally)
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16)
        # Find the color that occurs most often
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = palette[palette_index * 3:palette_index*3 + 3]
        colors.append(closest_color(dominant_color))

    with Image.open(os.path.join(pic_path, "right_half.png")) as img:
        img.thumbnail((100, 100))
        # Reduce colors (uses k-means internally)
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16)
        # Find the color that occurs most often
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = palette[palette_index* 3:palette_index*3 + 3]
        colors.append(closest_color(dominant_color))

    return colors


def loop():
    while True:
        sound.play(get_colors())

t1 = threading.Thread(target=get_image, name='t1')
t2 = threading.Thread(target=loop, name='t2')
t1.start()
t2.start()


