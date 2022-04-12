import os
import sys
import time
import sound
import threading
import colors
import pygame.camera
# import RPi.GPIO as GPIO
# import detect
from pygame.locals import *

# Setting directories for future use
dir_path = os.path.dirname(os.path.realpath(__file__))
pic_path = os.path.join(dir_path, "pics")

def get_image():
    pygame.camera.init()
    
    camlist = pygame.camera.list_cameras()
    if camlist == []:
        sys.exit("Camera Not Found")
    else:
        camera = pygame.camera.Camera(camlist[0],(640,480))

    for i in enumerate(camera.capture_continuous(os.path.join(pic_path, "img.jpg"), use_video_port=False)):
            time.sleep(2)


def loop():
    # button_pressed = False
    # GPIO.setwarnings(False) # Ignore warning for now
    # GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    # GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    sound.play(["one_beep", "one_beep"], True) # Letting User know that its in Color detection mode
    time.sleep(3)
    
    while True:
        while True:
        
            # if GPIO.input(10) == GPIO.HIGH:
            #     sound.play(["two_beep, two_beep"], True)
            #     break
            sound.play(colors.get_colors())
            time.sleep(.2)

        while True:
            if GPIO.input(10) == GPIO.HIGH:
                sound.play(["one_beep, one_beep"], True)
                break
            sound.play(detection.detect())
            

# t1 = threading.Thread(target=get_image, name='t1')
t2 = threading.Thread(target=loop, name='t2')
# t1.start()
t2.start()


