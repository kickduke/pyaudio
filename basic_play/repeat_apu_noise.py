#!/usr/bin/python3
import time
import pyaudio
import wave
import sys
import math
import struct

##写入wav流
def write_note(time, freq, framerate, file, vol, sampwidth):
    t = 0
    step = 1.0/framerate
    period = 8.0 * freq
    amp = vol * (math.pow(2, sampwidth*8 - 1))
    if freq > 0 :
        time_refine = round(time*freq,0)/freq
    else :
        time_refine = time
    while t <= time_refine :
        if (t*period) % 8.0 <= 8.0/(15) :    
            note = int(amp)
        else : 
            note = 0
        t += step
        file.writeframesraw(struct.pack('H',note))


#game
runnable = 1
GAMEFRAME = 60
frame_period = 1.0/GAMEFRAME
cnt = 0
noise_list = [4, 8, 16, 32, 64, 96, 128, 160, 202, 254, 380, 508, 762, 1016, 2034, 4068]
#audio
FRAMERATE = 44100
CHANNELS = 1
SAMPWIDTH = 2
linecnt = 0
wf = wave.open('APU_NOISE.wav', 'w')
wf.setnchannels(CHANNELS)
wf.setframerate(FRAMERATE)
wf.setsampwidth(SAMPWIDTH)
#source
sf = open('APU_NOISE_LOG.txt', 'r')
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
    wave_len_idx = int(readline.split(':', 3)[2])
    vol = int(readline.split(':', 3)[3])/15
    if noise_list[wave_len_idx] > 0 :
        note_freq = round((1.789773*1000000.0)/(16*(noise_list[wave_len_idx])),2)
    else :
        note_freq = 0
    print('cnt=' + str(cnt) + ' ' + str(wave_len_idx) + ' ' + str(note_freq) + ' ' + str(vol) )
    write_note(frame_period, note_freq, FRAMERATE, wf, vol, SAMPWIDTH)
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
wf = wave.open('APU_NOISE.wav', 'rb')
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
data = wf.readframes(CHUNK)   #每次读取n帧数据

while data != '':
    stream.write(data)  #数据写入缓冲流
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()   
