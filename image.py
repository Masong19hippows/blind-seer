import os
import sys
import time
import sound
import requests
import threading
import colors
import pygame.camera
# import keyboard
# import RPi.GPIO as GPIO
import detect
from pygame.locals import *

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

def get_image():
    pygame.camera.init()
    
    camlist = pygame.camera.list_cameras()
    print(camlist)
    if camlist == []:
        sys.exit("Camera Not Found")
    else:
        camera = pygame.camera.Camera(camlist[4],(640,480), "RGB")

    camera.start()
    while True:
        time.sleep(.5)
        image = camera.get_image()
        try:
            pygame.image.save(image, os.path.join(pic_path, "img.jpg"))
        except:
            time.sleep(.25)
            pygame.image.save(image, os.path.join(pic_path, "img.jpg"))


def loop():
    # GPIO.setwarnings(False) # Ignore warning for now
    # GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    # GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    sound.play(["one_beep", "one_beep"], True) # Letting User know that its in Color detection mode
    time.sleep(3)
    
    while True:
        while True:
            # if keyboard.read_key() == "x":
            #     try: 
            #         request = requests.get("https://google.com", timeout=3)
            #     except (requests.ConnectionError, requests.Timeout) as exception:
            #         sound.play(["no_internet", "no_internet"], True)
            #         time.sleep(.5)
            #         continue

            #     sound.play(["two_beep", "two_beep"], True)
            #     time.sleep(1.5)
            #     break
  
            sound.play(colors.get_colors())
            time.sleep(.2)
        while True:

            # if keyboard.read_key() == "p":
            #     sound.play(["one_beep", "one_beep"], True)
            #     time.sleep(1.5)
            #     break
            sound.play(detect.detect(), True)
            

t1 = threading.Thread(target=get_image, name='t1')
t2 = threading.Thread(target=loop, name='t2')
t1.start()
t2.start()


