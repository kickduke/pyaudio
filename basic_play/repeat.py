#!/usr/bin/python3
import time
import pyaudio
import wave
import sys
import math
import struct

##写入wav流
def write_note(time, freq, framerate, file, vol = 0.5, sampwidth = 2):
    t = 0   #时刻
    PCT = 50   #占空比
    step = 1.0/framerate    #每帧时长，用于计算t
    period = 2.0 * freq     #每秒震动周期，与频率正相关  假设每个方波周期是2.0
    amp = vol * (math.pow(2, sampwidth*8 - 1))
    while t <= time:
        note = int(amp/2*(t*period%2))
        t += step
        file.writeframesraw(struct.pack('h',note))   #转为short整型

#game
runnable = 1
GAMEFRAME = 60
frame_period = 1.0/GAMEFRAME
cnt = 0
#audio
FRAMERATE = 44100
CHANNELS = 2
g  = 196
c1 = 261.63
d1 = 293.66
e1 = 329.63
f1 = 349.23
g1 = 392
a1 = 440
b1= 493.88
wf = wave.open('tri_wave.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(2)
#source
sf = open('source.txt', 'r')

##生成音频
while(runnable != 0) :
    start_time = time.time()
    readline = sf.readline().replace('\n', '')
    cnt += 1
    print('cnt=' + str(cnt) + ' ' + readline.split(':', 1)[0] + ' ' + readline.split(':', 1)[1])
    write_note(frame_period, float(readline.split(':', 1)[1]), FRAMERATE, wf, 0.5, 2)
    end_time = time.time()
    sleep_time = frame_period - (end_time - start_time)
    if(sleep_time > 0) :
        time.sleep(sleep_time)
    if(cnt >= 240) :
        runnable = 0
        wf.close()
        sf.close()
        
##播放生成的wav文件
print('开始播放wav')
CHUNK = 1
wf = wave.open('tri_wave.wav', 'rb')
#rf = open('record.txt', 'w')
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
data = wf.readframes(CHUNK)   #每次读取n帧数据
#rf.write(str(data) + '\n')

while data != '':
    stream.write(data)  #数据写入缓冲流
    data = wf.readframes(CHUNK)
    #rf.write(str(data) + '\n')

stream.stop_stream()
stream.close()
rf.close()    
