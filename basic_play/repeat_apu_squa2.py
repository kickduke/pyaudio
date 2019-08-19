#!/usr/bin/python3
import time
import pyaudio
import wave
import sys
import math
import struct

##写入wav流
def write_note(time, freq, framerate, file, vol = 0.5, sampwidth = 2, duty = 2):
    t = 0   #时刻
    #占空比
    if duty == 0 :
        PCT = 12.5
    if duty == 1 :
        PCT = 25
    if duty == 2 :
        PCT = 50
    if duty == 3 :
        PCT = 75
    step = 1.0/framerate    #每帧时长，用于计算t
    period = 8.0 * freq     #每秒震动周期，与频率正相关  假设每个方波周期是8.0
    if freq > 0 :
        time_refine = round(time*freq, 0)/freq
    else :
        time_refine = time
    while t <= time_refine:
        if (t*period) % 8.0 <= 8.0/(100/PCT):    
            amp = vol * (math.pow(2, sampwidth*8 - 1))
        else: 
            amp = 0
        note = int(amp)
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
SAMPWIDTH = 1
DUTY = 2
g  = 196
c1 = 261.63
d1 = 293.66
e1 = 329.63
f1 = 349.23
g1 = 392
a1 = 440
b1= 493.88
linecnt = 0
wf = wave.open('APU_SUQA2.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(SAMPWIDTH)
#source
sf = open('APU_SQUA2_LOG.txt', 'r')
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
    wave_len = int(readline.split(':', 4)[2])  #波长
    vol = round(int(readline.split(':', 4)[3])/15,2)  #音量
    duty= int(int(readline.split(':', 4)[4]))  #占空比
    if wave_len > 0 :
        note_freq = round((1.789773*1000000.0)/(16*(wave_len+1)),2)
    else :
        note_freq = 0
    print('cnt=' + str(cnt) + ' ' + str(wave_len) + ' ' + str(note_freq) + ' ' + str(vol) + ' ' + str(duty))
    write_note(frame_period, note_freq, FRAMERATE, wf, vol, SAMPWIDTH, duty)
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
wf = wave.open('APU_SUQA2.wav', 'rb')
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
