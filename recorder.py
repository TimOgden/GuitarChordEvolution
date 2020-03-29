import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
import numpy as np
import pyaudio
import wave
import threading
import plot_spectrogram
import time

p = pyaudio.PyAudio()
rate = 44100
chunk = 1024
recording_length = 6
channels = 1
p_format = pyaudio.paInt16

start_threshold_silence = 1000
end_threshold_silence = 500

stream = p.open(format=p_format, channels=channels,
				rate=rate, input=True, frames_per_buffer=chunk)

def record_for_time(filename, time=recording_length, plt_wav=False):
	print('* recording')
	frames = []

	for i in range(int(rate/chunk*time)):
		data = stream.read(chunk)
		frames.append(data)
	print('* done recording')

	start = 0
	end = 0
	start_sec = 0
	end_sec = 0
	with wave.open(filename, 'wb') as f:
		f.setnchannels(channels)
		f.setsampwidth(p.get_sample_size(p_format))
		f.setframerate(rate)
		f.writeframes(b''.join(frames))

	with wave.open(filename, 'r') as f:
		start, end, start_sec, end_sec = find_whitespace(filename, frames)
		if(plt_wav):
			plot_wav(f, dispEnds=True, start=start, end=end)

	start_millis = int(start_sec * recording_length * 1000) # Convert to milliseconds
	end_millis = int(end_sec * recording_length * 1000)
	newAudio = AudioSegment.from_wav(filename)
	newAudio = newAudio[start_millis:end_millis]
	newAudio.export(filename, format='wav')

def find_whitespace(file, frames):
	[fs,x] = wavfile.read(file)
	start = 0
	for c, val in enumerate(x):
		if abs(val) >= start_threshold_silence:
			start = c
			break
	end = len(x) - 1
	for val in range(len(x)-1,-1,-1):
		if abs(x[val]) >= end_threshold_silence:
			break
		end -= 1
	return start, end, start/len(x), end/len(x)

def plot_wav(file, dispEnds=False, start=0, end=0):
	signal = file.readframes(-1)
	signal = np.fromstring(signal, 'Int16')
	plt.figure()
	plt.plot(signal)
	if dispEnds:
		plt.axvline(start, color='r')
		plt.axvline(end, color='r')
	plt.show()

def start_recording_thread(filename, time=recording_length, plt_wav=False):
	x = threading.Thread(target=record_for_time, args=(filename, time, plt_wav))
	x.start()

if __name__ == '__main__':
	start_recording_thread('./tmp/target.wav', time=5, plt_wav=True)
	time.sleep(5)
	plot_spectrogram.plot_spect('./tmp/target.wav','./tmp/target.png')