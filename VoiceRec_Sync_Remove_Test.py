import collections
import os
import sys
import time
import numpy as np
import getopt
# Import things for pocketsphinx
import pyaudio
import wave
import pocketsphinx as ps
#import sphinxbase

leds = collections.OrderedDict()
# Parameters for pocketsphinx
LMD   = "/home/root/led-speech-edison/lm/8484.lm"
DICTD = "/home/root/led-speech-edison/lm/8484.dic"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
PATH = 'output'

#randnum=''

#try:
#	opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#for opt, arg in opts:
#	if opt == '-i':
randnum=sys.argv[1]


#randnum=np.random.randint(1,1000)
cmd='/home/root/bin/ffmpeg/ffmpeg -f alsa -thread_queue_size 32768 -itsoffset -0.8 -ac 1 -t 15.8 -i hw:2 -f video4linux2 -thread_queue_size 8388608 -itsoffset 00:00 -s hd480 -t 15 -i /dev/video0 -b:v 1M -c:v libxvid -vsync cfr /home/root/Videos/voicerec%s.avi' %randnum
cmdpic='/home/root/bin/ffmpeg/ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 /home/root/Pictures/voicerec%s.jpeg' %randnum
def triggerLeds(leds, words):







    if "SYNCHRONIZE" in words:
        print 'SYNCHRONIZE'
    if "REMOVE" in words:
        print 'REMOVE'
    if "RECORD" in words:
        print 'RECORD'
	os.system(cmd)
       # os.system("/home/root/bin/ffmpeg/ffmpeg -f alsa -thread_queue_size 32768 -itsoffset -0.8 -ac 1 -t 15.8 -i hw:2 -f video4linux2 -thread_queue_size 8388608 -itsoffset 00:00 -s hd480 -t 15 -i /dev/video0 -b:v 1M -c:v libxvid -vsync cfr /home/root/Videos/vrtestname%d.avi" %randnum) )
    if "PICTURE" in words:
        print 'PICTURE'
	os.system(cmdpic)	
	#os.system("THIS IS WHERE THE PICTURE COMMAND GOES")





def decodeSpeech(speech_rec, wav_file):
	wav_file = file(wav_file,'rb')
	wav_file.seek(44)
	speech_rec.decode_raw(wav_file)
	result = speech_rec.get_hyp()
	return result[0]

def main():
    # Set direction of LED controls to out

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    p = pyaudio.PyAudio()
    speech_rec = ps.Decoder(lm=LMD, dict=DICTD)

    #while True:
    if True:
        # Record audio
    	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    	print("* recording")
    	frames = []
    	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    		data = stream.read(CHUNK)
    		frames.append(data)
    	print("* done recording")
    	stream.stop_stream()
    	stream.close()
    	#p.terminate()

        # Write .wav file
        fn = "o.wav"
    	wf = wave.open(os.path.join(PATH, fn), 'wb')
    	wf.setnchannels(CHANNELS)
    	wf.setsampwidth(p.get_sample_size(FORMAT))
    	wf.setframerate(RATE)
    	wf.writeframes(b''.join(frames))
    	wf.close()

        # Decode speech
    	wav_file = os.path.join(PATH, fn)
    	recognised = decodeSpeech(speech_rec, wav_file)
    	rec_words = recognised.split()


        triggerLeds(leds, rec_words)
        # Playback recognized word(s)
    	cm = 'espeak "'+recognised+'"'
    	os.system(cm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupt received. Cleaning up..."
