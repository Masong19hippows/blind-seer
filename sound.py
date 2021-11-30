import image
import pygame
import os
import soundfile
from gtts import gTTS


dir_path = os.path.dirname(os.path.realpath(__file__))

def play():
    pygame.mixer.init() 
    color = image.get_color()
    tts = gTTS(text=color[0], lang='en')
    tts.save("colorleft.wav")
    tts = gTTS(text=color[1], lang='en')
    tts.save("colorright.wav")
    pygame.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)
    pygame.mixer.set_num_channels(2)
    m = pygame.mixer.Sound(os.path.join(dir_path, 'colorleft.wav'))
    n = pygame.mixer.Sound(os.path.join(dir_path, 'colorright.wav'))
    pygame.mixer.Channel(1).play(m,-1)
    pygame.mixer.Channel(2).play(n,-1)
play()
