import numpy as np
from chord import Chord
from guitar import Guitar
import matplotlib.pyplot as plt
from recorder import start_recording_thread
from plot_spectrogram import plot_spect
import time
from misc_tools import TwoWayDict
import chord_breeder

pop = []
n_rows, n_cols = 2,4
first_place_bonus = 3
second_place_bonus = 2
third_place_bonus = 1
MAX_POP_SIZE = n_rows * n_cols
NUM_STEPS = 100

def convert_to_spectrogram(filename='./tmp/guess.wav'):
	png_file = filename[:-4] + '.png'
	return plot_spect(filename, png_file, eval_fitness=True)

def record_and_eval(chord):
	_, frets = Guitar.read_chord(chord)
	start_recording_thread('./tmp/guess.wav')
	Guitar.play_chord(frets)
	time.sleep(2)
	return convert_to_spectrogram()

def find_empty_spot(chord_pos):
	for chord in chord_pos.values():
		if type(chord) != Chord:
			continue
		if not chord.alive:
			return chord_pos[chord]
	return None

if __name__ == "__main__":
	# Initializing the population randomly
	f, axs = plt.subplots(n_rows, n_cols, sharex=True)
	chord_pos = TwoWayDict()
	
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
	
	print(len(pop))
	Guitar.openJVM()

	# Repeat following for x number of steps:
	for step in range(NUM_STEPS):
		for i in range(MAX_POP_SIZE):
			plt.subplot(n_rows, n_cols, i+1)
			chord = Chord()
			chord_pos[chord] = i+1
			chord.plot_chord()
			plt.title('')
			pop.append(chord)
		plt.pause(0.05)
		# **Calculate and assign fitness to each organism**
		# - Start recording
		# - play chord by guitar.py
		# - convert wav to spectrogram by plot_spectrogram.py
		# - fitness = MSE(target image, guess image)
		for c, chord in enumerate(pop):
			fitness = record_and_eval(chord)
			chord.fitness = fitness
			print('f={}'.format(fitness))
			plt.subplot(n_rows,n_cols,c+1)
			plt.title('f={}'.format(round(fitness,2)))
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
			pop.remove(chord)
			plt.pause(0.5)

		# **Breed the organisms to refill the population**
		# - Lowest fitness should breed the most
		# - Use chord_breeder.py to generate offspring
		candidates = []
		for chord in pop[int(len(pop)/2):]:
			candidates.append(chord)
		[candidates.append(candidates[0]) for _ in range(first_place_bonus-1)]
		[candidates.append(candidates[1]) for _ in range(second_place_bonus-1)]
		[candidates.append(candidates[2]) for _ in range(third_place_bonus-1)]
		candidates = np.random.permutation(np.array(candidates))
		print(candidates)

		diff = MAX_POP_SIZE - len(pop)
		for i in range(diff):
			if(len(pop)>=MAX_POP_SIZE):
				break
			try:
				chord = chord_breeder.breed(candidates[i*2], candidates[i*2+1], debug=True)
				
				pop.append(chord)

				chord_pos[chord] = find_empty_spot(chord_pos)
			except:
				pass
		plt.pause(1)
	Guitar.closeJVM()