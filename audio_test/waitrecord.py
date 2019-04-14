# based off of skeleton from https://stackoverflow.com/questions/19070290/pyaudio-listen-until-voice-is-detected-and-then-record-to-a-wav-file

import threading
from array import array
from queue import Queue, Full
import wave
import os

import pyaudio


CHUNK_SIZE = 1024

# minimum volume to start recording. 3000 is arbitrary
MIN_VOLUME = 3000
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10

# frame buffer for audio data
frames = []
# counter to keep track of silence length
silencecounter = 0
# threshold for when to stop recording 
silencethreshold = 100
# counter to keep track of the session number to save
counter = 0
# indicator to show when stuff is recording 
record = 0

# filename header
wav_output_filename = 'test'

# start audio stream
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024,
)

# main() method starts threads
def main():
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, q))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


# record method takes an audio chunk from the listen thread and processes it
def record(stopped, q):
    global silencecounter
    global silencethreshold
    global counter
    global record
    global frames
    global audio

    while True:
        if stopped.wait(timeout=0):
            break
        chunk = q.get()
        vol = max(chunk)
        
        if vol >= MIN_VOLUME:
            # start recording and/or write audio data to frames
            frames.append(chunk)
            print("O")
            silencecounter = 0
            record = 1
        else:
            # if not recording, keep not recording. if recording, keep recording. if recording and silence counter reaches threshold, save stuff
            print("-")
            silencecounter += 1
            if record == 1:
                frames.append(chunk)
            if silencecounter > silencethreshold and record == 1:
                print("saving")
                form_1 = pyaudio.paInt16
                # variables. TODO move these variables to the top
                chans=1
                samp_rate = 44100
                chunk = 1024
                record_secs = 1     #record time
                dev_index = 0
                wavefile=wave.open(wav_output_filename + repr(counter) + ".wav",'wb')
                wavefile.setnchannels(chans)
                wavefile.setsampwidth(audio.get_sample_size(form_1))
                wavefile.setframerate(samp_rate)
                wavefile.writeframes(b''.join(frames))
                wavefile.close()
                # reset indicators
                record = 0
                counter += 1
                frames = []


# listen stream. doesn't do anything except write sound to buffer
def listen(stopped, q):
    global stream

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(array('h', stream.read(CHUNK_SIZE)))
        except Full:
            pass  # discard

# start main stuff
if __name__ == '__main__':
    main()