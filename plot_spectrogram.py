import matplotlib.pyplot as plt
from scipy.io import wavfile
from imageio import imwrite
from scipy import signal
import sys
import numpy as np
import cv2
frequencies = None
def plot_spect(file, output, plot_plt=False):
	sample_rates, samples = wavfile.read(file)
	frequencies, times, spectrogram = signal.spectrogram(samples, sample_rates, nfft=2048, noverlap=1800, nperseg=2048)
	print('frequencies:',frequencies.shape)
	print('times:',times.shape)
	print('spectrogram:',spectrogram.shape)
	if(plot_plt):
		fig = plt.figure(frameon=False)
		try:
			plt.pcolormesh(times, frequencies, 10*np.log(spectrogram))
		except Exception as e:
			print('Exception:',e)
		plt.ylabel('Frequency [Hz]')
		plt.xlabel('Time [sec]')
		plt.title(file[:-4])
		plt.ylim(top=8000)
		plt.axhline(y=1318.51, linewidth=1)
		plt.show()
	imwrite(output, 10*np.log10(spectrogram))
	return frequencies

def MSE(guess, target='./tmp/target.png'):
	target = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
	target = np.mean(target,axis=1)
	guess = np.mean(cv2.imread(guess, cv2.IMREAD_GRAYSCALE),axis=1)
	return (np.square(guess - target)).mean(axis=None)

def AE(guess, target='./tmp/target.png'):
	target = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
	target = np.mean(target,axis=1)
	guess = np.mean(cv2.imread(guess, cv2.IMREAD_GRAYSCALE),axis=1)
	return (guess - target).mean(axis=None)

def one_hot(img, threshold=214):
	img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
	maximum = np.amax(img)
	img = np.divide(img, maximum) # Normalize image
	img = np.multiply(img, 255)
	img = np.mean(img, axis=1)
	print(frequencies[np.argmax(img)])
	binary_img = np.where(img < threshold, 0, 255)
	binary_img = np.reshape(binary_img, (binary_img.shape[0],1))
	plt.imshow(np.repeat(binary_img, 256, axis=1))
	plt.show()


if __name__ == '__main__':
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	frequencies = plot_spect(file2, './tmp/target_real.png', plot_plt=True)
	#one_hot(file1)
	#freq1 = plot_spect(file2, './tmp/target_real.png', plot_plt=False)
	#print(freq1[5],freq1[6],freq1[11])