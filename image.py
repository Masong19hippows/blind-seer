import image_slicer
import os
import shutil
import cv2
import numpy as np
from skimage import io

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

# Slicing image from raspberry pi into 2 images from left to right.
def slice():
    image_slicer.slice(os.path.join(pic_path, "download.png"), 2)
    shutil.move(os.path.join(pic_path, "download_01_01.png"), os.path.join(pic_path, "first_half.png"))
    shutil.move(os.path.join(pic_path, "download_01_02.png"), os.path.join(pic_path, "second_half.png"))


# Getting the most dominant color (using k-means clustering) in the 2 images and outputting it as rgb values for both left and right
def get_color():

    # Slicing the image and setting variables that refrence both the split images
    slice()
    img1 = io.imread(os.path.join(pic_path, "first_half.png"))[:, :, :-1]
    img2 = io.imread(os.path.join(pic_path, "second_half.png"))[:, :, :-1]

    # Getting the dominant color of both images
    pixels1 = np.float32(img1.reshape(-1, 3))
    pixels2 = np.float32(img2.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels1, palette1 = cv2.kmeans(pixels1, 5, None, criteria, 10, flags)
    _, labels2, palette2 = cv2.kmeans(pixels2, 5, None, criteria, 10, flags)
    _, counts1 = np.unique(labels1, return_counts=True)
    _, counts2 = np.unique(labels2, return_counts=True)

    # Returning the domanint color in both images in a RGB value list
    list = np.append(palette1[np.argmax(counts1)], palette2[np.argmax(counts2)])
    return list
    
