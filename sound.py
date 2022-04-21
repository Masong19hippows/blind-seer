import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import gtts
import shutil
import wave




dir_path = os.path.dirname(os.path.realpath(__file__))
sound_path = os.path.join(dir_path, "sounds")
pygame.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)



def play(sounds,both = False):
    left = None
    right = None
    print(sounds)
    for file in os.listdir(sound_path):
        file_name = os.path.splitext(file)[0]
        if file_name == sounds[0]:
            left = os.path.join(sound_path, str(file_name) + ".wav")
        if both == False:
            if file_name == sounds[1]:
                right = os.path.join(sound_path, str(file_name) + ".wav")
    for file in os.listdir(os.path.join(sound_path, "new")):
        file_name = os.path.splitext(file)[0]
        if file_name == sounds[0]:
            left = os.path.join(sound_path, "new", str(file_name) + ".wav")
        if both == False:
            if file_name == sounds[1]:
                right = os.path.join(sound_path, "new", str(file_name) + ".wav")

    if both == True:
        if left == None:
            gtts.gTTS(sounds[0]).save(os.path.join(sound_path, "new", str(sounds[0]) + ".wav"))
            os.system(f'ffmpeg -i "{os.path.join(sound_path, "new", str(sounds[0]) + ".wav")}" "{os.path.join(sound_path, "new", str(sounds[0]) + "t.wav")}"')
            shutil.move(os.path.join(sound_path, "new", str(sounds[0]) + "t.wav"), os.path.join(sound_path, "new", str(sounds[0]) + ".wav"))
            spf = wave.open(os.path.join(sound_path, "new", str(sounds[0]) + ".wav"), 'rb')
            RATE = spf.getframerate()
            signal = spf.readframes(-1)
            wf = wave.open(os.path.join(sound_path, "new", str(sounds[0]) + ".wav"), 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(RATE*1.6)
            wf.writeframes(signal)
            wf.close()
            spf.close()
            left = os.path.join(sound_path, "new", str(sounds[0]) + ".wav")

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