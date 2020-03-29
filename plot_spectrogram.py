import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.misc import imsave
from scipy import signal
import sys
import numpy as np
import cv2

def plot_spect(file, output, plot_plt=False, eval_fitness=False):
	sample_rates, samples = wavfile.read(file)
	frequencies, times, spectrogram = signal.spectrogram(samples,sample_rates, nfft=2048, noverlap=1800, nperseg=2048)
	if(plot_plt):
		fig = plt.figure(frameon=False)
		try:
			plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram))
		except Exception as e:
			print('Exception:',e)
		plt.ylabel('Frequency [Hz]')
		plt.xlabel('Time [sec]')
		plt.title(file[:-4])
		plt.ylim(top=8000)
		plt.show()
	imsave(output, 10*np.log10(spectrogram)[:528,:])
	if(eval_fitness):
		return MSE(output)

def MSE(guess):
	target = cv2.imread('./tmp/target.png', cv2.IMREAD_GRAYSCALE)
	target = np.mean(target,axis=1)
	guess = np.mean(cv2.imread(guess, cv2.IMREAD_GRAYSCALE),axis=1)
	return (np.square(guess - target)).mean(axis=None)

def AE():
	target = cv2.imread('./tmp/1.png', cv2.IMREAD_GRAYSCALE)
	guess = cv2.resize(cv2.imread('./tmp/0.png', cv2.IMREAD_GRAYSCALE), (target.shape[1], target.shape[0]))
	return np.absolute(guess-target).mean(axis=None)

if __name__ == '__main__':
	guess = sys.argv[1]
	plot_spect(guess, './tmp/guess.png', plot_plt=True)