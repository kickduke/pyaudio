import pyaudio
import wave
import sys



CHUNK = 1024

wf = wave.open(r'D:\\PythonProject\\pyaudio\kchcl.wav', 'rb')
rf = open('record.txt','w')

p = pyaudio.PyAudio()

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),  #2
                channels = wf.getnchannels(), #2
                rate = wf.getframerate(),     #44100
                output = True)

#data = wf.readframes(CHUNK)   #每次读取1024帧数据
data = wf.readframes(1)
rf.write(str(data) + '\n')

while data != '':
    stream.write(data)
    #data = wf.readframes(CHUNK)
    data = wf.readframes(1)
    rf.write(str(data)+ '\n')

stream.stop_stream()
stream.close()
rf.close()

p.terminate()
