import pickle
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
	num = int(sys.argv[1])
	with open('best.pickle', 'rb') as f:
		pop = pickle.load(f)
	for i in range(num):
		plt.subplot(1,num,i+1)
		plt.title('Chord {} f={}'.format(i+1, int(pop[i].fitness)))
		pop[i].plot_chord()
	plt.show()