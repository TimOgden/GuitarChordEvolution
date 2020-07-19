import librosa
import librosa.display
from scipy.io import wavfile
from scipy.signal import argrelextrema
import sys
import numpy as np
import matplotlib.pyplot as plt

notes = ['C1','C#1','D1','D#1','E1','F1','F#1','G1','G#1','A1','A#1','B1',
		'C2','C#2','D2','D#2','E2','F2','F#2','G2','G#2','A2','A#2','B2',
		'C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3',
		'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
		'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
		'C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6',
		'C7','C#7','D7','D#7','E7','F7','F#7','G7','G#7','A7','A#7','B7']
def local_maxes():
	maxes = []
	for c, value in enumerate(avgs):
		if c==0:

			maxes.append()

def analyze(filename, plot_q_transform=False, debug=False,hops_multiplier=0):
	sample_rates, samples = wavfile.read(filename)
	samples = np.asfortranarray(samples)
	q_transform = librosa.core.cqt(np.reshape(samples, (samples.shape[0],)),
		sr=sample_rates, hop_length=512*2**hops_multiplier)
	#librosa.display.specshow(librosa.amplitude_to_db(q_transform, ref=np.max),
	#							sr=sample_rates, x_axis='time', y_axis='cqt_note')
	#librosa.display.specshow(q_transform,
	#							sr=sample_rates, x_axis='time', y_axis='cqt_hz')
	avgs = np.mean(q_transform, axis=1)
	avgs = np.where(abs(avgs) > np.percentile(abs(avgs),87), avgs, 0)
	indices_of_extrema = argrelextrema(avgs, np.greater)[0].astype(np.int)
	#print('Indices:', indices_of_extrema)
	resulting_freq = []
	resulting_notes = []
	for index in indices_of_extrema:
		try:
			resulting_freq.append(2**(index/12)*32.7)
			resulting_notes.append(notes[index])
		except IndexError as e:
			print(e, index)
	if debug:
		print('Audio analysis results:', resulting_freq, resulting_notes)
	avgs_img = np.repeat(np.reshape(abs(avgs), (avgs.shape[0],1)), 256, axis=1)
	if plot_q_transform:
		librosa.display.specshow(avgs_img,
									sr=sample_rates, x_axis='time', y_axis='cqt_note')
		plt.tight_layout()
		plt.show()
	return resulting_freq


if __name__ == '__main__':
	filename = sys.argv[1]
	print(analyze(filename, plot_q_transform=True, debug=True,hops_multiplier=1))