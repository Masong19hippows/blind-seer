import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sound_path = os.path.join(dir_path, "sounds")
pygame.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)


def play(sounds,both = False):
    print(sounds)
    for file in os.listdir(sound_path):
        file_name = os.path.splitext(file)[0]
        if file_name == sounds[0]:
            left = os.path.join(sound_path, str(file_name) + ".wav")
        if both == False:
            if file_name == sounds[1]:
                right = os.path.join(sound_path, str(file_name) + ".wav")


    if both == False:
        sound0 = pygame.mixer.Sound(left)
        sound1 = pygame.mixer.Sound(right)
        pygame.mixer.Channel(1).set_volume(1.0, 0.0)
    
        pygame.mixer.Channel(2).set_volume(0.0, 1.0)

        pygame.mixer.Channel(1).play(sound0)
        while pygame.mixer.Channel(1).get_busy():
            pygame.time.delay(1)
        time.sleep(.25)
        pygame.mixer.Channel(2).play(sound1)
        while pygame.mixer.Channel(2).get_busy():
            pygame.time.delay(1)

    else:
        sound0 = pygame.mixer.Sound(left)
        pygame.mixer.Channel(1).set_volume(1.0, 1.0)
        pygame.mixer.Channel(1).play(sound0)
        while pygame.mixer.Channel(1).get_busy():
            pygame.time.delay(1)