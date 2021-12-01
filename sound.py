import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from gtts import gTTS


dir_path = os.path.dirname(os.path.realpath(__file__))
sound_path = os.path.join(dir_path, "pics")

def play(colors):
    tts = gTTS(text=colors[0], lang='en',  slow=False)
    tts.save(os.path.join(sound_path, "colorleftOG.wav"))
    tts = gTTS(text=colors[1], lang='en',  slow=False)
    tts.save(os.path.join(sound_path, "colorrightOG.wav"))
    os.system(f"ffmpeg -y -i {os.path.join(sound_path, 'colorleftOG.wav')} {os.path.join(sound_path, 'colorleft.wav')}  > /dev/null 2>&1")
    os.system(f"ffmpeg -y -i {os.path.join(sound_path, 'colorrightOG.wav')} {os.path.join(sound_path, 'colorright.wav')}  > /dev/null 2>&1")

    pygame.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)

    sound0 = pygame.mixer.Sound(os.path.join(sound_path, 'colorleft.wav'))
    sound1 = pygame.mixer.Sound(os.path.join(sound_path, 'colorright.wav'))

    pygame.mixer.Channel(1).set_volume(1.0, 0.0)
    pygame.mixer.Channel(2).set_volume(0.0, 1.0)
    pygame.mixer.Channel(1).play(sound0)
    while pygame.mixer.Channel(1).get_busy():
        pygame.time.delay(10)
    pygame.mixer.Channel(2).play(sound1)
    while pygame.mixer.Channel(2).get_busy():
        pygame.time.delay(10)
