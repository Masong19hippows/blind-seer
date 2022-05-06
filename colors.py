import os
import time
import shutil
from image_slicer import slice
from PIL import Image
from PIL import UnidentifiedImageError
from math import sqrt

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")


# Slicing image from raspberry pi into 2 images from left to right.
def slice_image():
    try:
        slice(os.path.join(pic_path, "img.jpg"), 2)
    except UnidentifiedImageError:
        time.sleep(.25)
        slice(os.path.join(pic_path, "img.jpg"), 2)
        
    shutil.move(os.path.join(pic_path, "img_01_01.png"), os.path.join(pic_path, "left_half.png"))
    shutil.move(os.path.join(pic_path, "img_01_02.png"), os.path.join(pic_path, "right_half.png"))

Colors = {
    # 'black': (0, 0, 0),
    # 'white': (255, 255, 255),
    'red': (128, 0, 0), 
    'lime': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    # 'cyan': (0, 255, 255),
    # 'magenta': (255, 0, 255),
    'silver': (192, 192, 192),
    # 'gray': (128, 128, 128),
    'maroon': (128, 0, 0),
    'olive': (128, 128, 0),
    'green': (0, 128, 0),
    # 'purple': (128, 0, 128),
    # 'teal': (0, 128, 128),
    # 'navy': (0, 0, 128),
    'orange': (255, 165, 0),
    # 'brown': (165, 42, 42)
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
    slice_image()

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