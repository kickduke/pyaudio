#!/usr/bin/python3
import time
import pyaudio
import wave
import sys
import math
import struct

##写入wav流
def write_note(time, framerate, file, sampwidth, freq1, vol1, duty1, freq2, vol2, duty2, freq3, vol3):
    t = 0   #时刻
    #占空比
    if duty1 == 0 :
        PCT1 = 12.5
    if duty1 == 1 :
        PCT1 = 25
    if duty1 == 2 :
        PCT1 = 50
    if duty1 == 3 :
        PCT1 = 75
    if duty2 == 0 :
        PCT2 = 12.5
    if duty2 == 1 :
        PCT2 = 25
    if duty2 == 2 :
        PCT2 = 50
    if duty2 == 3 :
        PCT2 = 75
    step = 1.0/framerate    #每帧时长，用于计算t
    period1 = 8.0 * freq1     #每秒震动周期，与频率正相关  假设每个方波周期是8.0
    period2 = 8.0 * freq2    
    if freq1 > 0 :
        time_refine1 = round(time*freq1, 0)/freq1
    else :
        time_refine1 = time
    if freq2 > 0 :
        time_refine2 = round(time*freq2, 0)/freq2
    else :
        time_refine2 = time
    #取较长的时间作为refine time，并记录哪个声道时间较短
    time_refine = max(time_refine1, time_refine2)
    time_shorter = min(time_refine1, time_refine2)
    if time_refine1 >= time_refine2 :
        shorter_channel = 2
    else :
        shorter_channel = 1

    amp1 = vol1 * (math.pow(2, sampwidth*8 - 1))
    amp2 = vol2 * (math.pow(2, sampwidth*8 - 1))
    while t <= time_refine:
        if t <= shorter_channel:
            if (t*period1) % 8.0 <= 8.0/(100/PCT1):    
                note1 = int(amp1)
            else: 
                note1 = 0
            if (t*period2) % 8.0 <= 8.0/(100/PCT2):    
                note2 = int(amp2)
            else: 
                note2 = 0
        else:
            if shorter_channel == 1 :
                note1 = 0
                if (t*period2) % 8.0 <= 8.0/(100/PCT2):    
                    note2 = int(amp2)
                else: 
                    note2 = 0
            if shorter_channel == 2 :
                note2 = 0
                if (t*period1) % 8.0 <= 8.0/(100/PCT1):    
                    note1 = int(amp1)
                else: 
                    note1 = 0
        #混频
        note = int(note1 + note2 - note1*note2/(math.pow(2, sampwidth*8 - 1)))
        t += step
        file.writeframesraw(struct.pack('H',note))   #转为short整型


#game
runnable = 1
GAMEFRAME = 60
frame_period = 1.0/GAMEFRAME
cnt = 0
#audio
FRAMERATE = 44100
CHANNELS = 1
SAMPWIDTH = 2
linecnt = 0
wf = wave.open('APU_MIX.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(SAMPWIDTH)
#source
sf1 = open('APU_SQUA1_LOG.txt', 'r')
sf2 = open('APU_SQUA2_LOG.txt', 'r')
sf3 = open('APU_TRI_LOG.txt', 'r')
##获取文件行数
for line in sf1.readlines() :
    linecnt += 1
print('linecnt=',linecnt)
sf1.seek(0)

##生成音频
while(runnable != 0) :
    start_time = time.time()
    readline1 = sf1.readline().replace('\n', '')
    readline2 = sf2.readline().replace('\n', '')
    readline3 = sf3.readline().replace('\n', '')
    cnt += 1
    wave_len1 = int(readline1.split(':', 4)[2])  #波长
    vol1 = round(int(readline1.split(':', 4)[3])/15,2)  #音量
    duty1 = int(int(readline1.split(':', 4)[4]))  #占空比
    if wave_len1 > 0 :
        note_freq1 = round((1.789773*1000000.0)/(16*(wave_len1+1)),2)
    else :
        note_freq1 = 0
    wave_len2 = int(readline2.split(':', 4)[2])  #波长
    vol2 = round(int(readline2.split(':', 4)[3])/15,2)  #音量
    duty2 = int(int(readline2.split(':', 4)[4]))  #占空比
    if wave_len2 > 0 :
        note_freq2 = round((1.789773*1000000.0)/(16*(wave_len2+1)),2)
    else :
        note_freq2 = 0
    wave_len3 = int(readline3.split(':', 2)[2])  #波长
    vol3 = 0.5        
    print('cnt=' + str(cnt) + ' ||squa1: ' + str(wave_len1) + ' ' + str(note_freq1) + ' ' + str(vol1) + ' ' + str(duty1) \
           + ' ||squa2: ' + str(wave_len2) + ' ' + str(note_freq2) + ' ' + str(vol2) + ' ' + str(duty2) + '||tri: ' + str(note_freq3))
    write_note(frame_period, FRAMERATE, wf, SAMPWIDTH, note_freq1, vol1, duty1, note_freq2, vol2, duty2, note_freq3, vol3)
    end_time = time.time()
    sleep_time = frame_period - (end_time - start_time)
    if(sleep_time > 0) :
        time.sleep(sleep_time)
    if(cnt >= linecnt) :
        runnable = 0
        wf.close()
        sf1.close()
        sf2.close()
        sf3.close()
        
##播放生成的wav文件
print('开始播放wav')
CHUNK = 1
wf = wave.open('APU_MIX.wav', 'rb')
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
