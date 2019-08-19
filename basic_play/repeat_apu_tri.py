#!/usr/bin/python3
import time
import pyaudio
import wave
import sys
import math
import struct

##写入wav流
def write_note(time, freq, framerate, file, vol = 0.5, sampwidth = 2):
    t = 0
    step = 1.0/framerate
    period = 1.0 * freq
    amp = vol * (math.pow(2, sampwidth*8 - 1))
    if freq > 0 :
        time_refine = round(time*freq,0)/freq
    else :
        time_refine = time
    while t <= time_refine :
        ##note = int(amp*(2*abs(2*(t*period - math.floor(t*period + 0.5))) - 1))
        note = int(amp*(abs(2*(t*period - math.floor(t*period + 0.5)))))
        t += step
        file.writeframesraw(struct.pack('h',note))


#game
runnable = 1
GAMEFRAME = 60
frame_period = 1.0/GAMEFRAME
cnt = 0
#audio
FRAMERATE = 44100
CHANNELS = 2
SAMPWIDTH = 1
g  = 196
c1 = 261.63
d1 = 293.66
e1 = 329.63
f1 = 349.23
g1 = 392
a1 = 440
b1= 493.88
linecnt = 0
wf = wave.open('APU.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(SAMPWIDTH)
#source
sf = open('APU_LOG.txt', 'r')
##获取文件行数
for line in sf.readlines() :
    linecnt += 1
print('linecnt=',linecnt)
sf.seek(0)

##生成音频
while(runnable != 0) :
    start_time = time.time()
    readline = sf.readline().replace('\n', '')
    cnt += 1
    wave_len = int(readline.split(':', 2)[2])
    if wave_len > 0 :
        note_freq = round((1.789773*1000000.0)/(16*(wave_len+1)),2)
    else :
        note_freq = 0
    print('cnt=' + str(cnt) + ' ' + str(wave_len) + ' ' + str(note_freq))
    write_note(frame_period, note_freq, FRAMERATE, wf, 0.5, SAMPWIDTH)
    end_time = time.time()
    sleep_time = frame_period - (end_time - start_time)
    if(sleep_time > 0) :
        time.sleep(sleep_time)
    if(cnt >= linecnt) :
        runnable = 0
        wf.close()
        sf.close()
        
##播放生成的wav文件
print('开始播放wav')
CHUNK = 1
wf = wave.open('APU.wav', 'rb')
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
