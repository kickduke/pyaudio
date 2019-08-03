import pyaudio
import wave
import sys
import math
import struct

##生成wav文件
def write_note(time, freq, framerate, file, vol = 0.5, sampwidth = 2):
    t = 0
    step = 1.0/framerate
    period = 1.0 * freq
    amp = vol * (math.pow(2, sampwidth*8 - 1))
    while t <= time:
        note = int(amp*(2*abs(2*(t*period - math.floor(t*period + 0.5))) - 1))
        t += step
        file.writeframesraw(struct.pack('h',note))
        

FRAMERATE = 12800
CHANNELS = 2
wf = wave.open('tri_wave.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(2)

g  = 196
c1 = 261.63
d1 = 293.66
e1 = 329.63
f1 = 349.23
g1 = 392
a1 = 440
b1= 493.88
#1231|1231
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, d1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, d1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
#3450|3450
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, f1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, 0, FRAMERATE, wf, 0.5, 2)
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, f1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, 0, FRAMERATE, wf, 0.5, 2)
#565431|565431
write_note(0.25, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, a1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, f1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, a1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, g1, FRAMERATE, wf, 0.5, 2)
write_note(0.25, f1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, e1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
#2510|2510
write_note(0.5, d1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, g, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, 0, FRAMERATE, wf, 0.5, 2)
write_note(0.5, d1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, g, FRAMERATE, wf, 0.5, 2)
write_note(0.5, c1, FRAMERATE, wf, 0.5, 2)
write_note(0.5, 0, FRAMERATE, wf, 0.5, 2)
wf.close()

##播放生成的wav文件
CHUNK = 1
wf = wave.open('tri_wave.wav', 'rb')
rf = open('record.txt', 'w')
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
data = wf.readframes(CHUNK)   #每次读取n帧数据
rf.write(str(data) + '\n')

while data != '':
    stream.write(data)  #数据写入缓冲流
    data = wf.readframes(CHUNK)
    rf.write(str(data) + '\n')

stream.stop_stream()
stream.close()
rf.close()





