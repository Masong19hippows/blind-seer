# This is for adding left and right sound based on the color of images.
import math
import pyaudio
from image import get_color

color = get_color()
PyAudio = pyaudio.PyAudio
real_color = color[0] + color[1] + color[2]
#See https://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000     #number of frames per second/frameset.      


FREQUENCY = real_color    #Hz, waves per second, 261.63=C4-note.
LENGTH = 5

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    

#generating wawes
for x in range(NUMBEROFFRAMES):
 WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

for x in range(RESTFRAMES): 
 WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()