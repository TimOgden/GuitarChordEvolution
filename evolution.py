import numpy as np
from chord import Chord
from guitar import Guitar
import matplotlib.pyplot as plt
from recorder import start_recording_thread
from plot_spectrogram import plot_spect
import time
from misc_tools import TwoWayDict

pop = []
NUM_STEPS = 100

def convert_to_spectrogram(filename='./tmp/guess.wav'):
	png_file = filename[:-4] + '.png'
	return plot_spect(filename, png_file, eval_fitness=True)

def record_and_eval(chord):
	_, frets = Guitar.read_chord(chord)
	start_recording_thread('./tmp/guess.wav')
	Guitar.play_chord(frets)
	time.sleep(3)
	return convert_to_spectrogram()

if __name__ == "__main__":
	# Initializing the population randomly
	n_rows, n_cols = 2,4
	MAX_POP_SIZE = n_rows * n_cols
	f, axs = plt.subplots(n_rows, n_cols, sharex=True)
	chord_pos = TwoWayDict()
	for i in range(MAX_POP_SIZE):
		plt.subplot(n_rows, n_cols, i+1)
		chord = Chord()
		chord_pos[chord] = i+1
		chord.plot_chord()
		pop.append(chord)
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
	plt.pause(0.05)
	print(len(pop))
	Guitar.openJVM()
	# Repeat following for x number of steps:
	for step in range(NUM_STEPS):
		# **Calculate and assign fitness to each organism**
		# - Start recording
		# - play chord by guitar.py
		# - convert wav to spectrogram by plot_spectrogram.py
		# - fitness = MSE(target image, guess image)
		for c, chord in enumerate(pop):
			fitness = record_and_eval(chord)
			chord.fitness = fitness
			print(fitness)
			plt.subplot(n_rows,n_cols,c+1)
			plt.title(round(fitness,2))
			plt.pause(0.05)
		# **Kill the weakest chords**
		# The bottom 50% or so of the population in terms of fitness
		# will be eliminated and will not have a chance to breed.
		# - sort by fitness
		# - remove the bottom half
		pop.sort(key=lambda x: (x.fitness))
		for c, chord in enumerate(pop[:int(len(pop)/2)]):
			plt.subplot(n_rows, n_cols,chord_pos[chord])
			plt.title('Killed')
			chord.alive = False
			plt.pause(0.05)
		plt.show()
		# **Breed the organisms to refill the population**
		# - Lowest fitness should breed the most
		# - Use chord_breeder.py to generate offspring

	Guitar.closeJVM()