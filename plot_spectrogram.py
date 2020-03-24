import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys
if __name__ == '__main__':
	filename = sys.argv[1]
	fs, data = wavfile.read(filename)
	plt.plot(data)
	plt.show()