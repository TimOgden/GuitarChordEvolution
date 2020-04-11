import numpy as np
from chord import Chord
from guitar import Guitar
import matplotlib.pyplot as plt
from recorder import start_recording_thread
from plot_spectrogram import plot_spect
import time
from misc_tools import TwoWayDict
import chord_breeder
import matplotlib.patches as patches

pop = []
avg_fitness = []
n_rows, n_cols = 2,4
first_place_bonus = 2
second_place_bonus = 1
third_place_bonus = 0
MAX_POP_SIZE = n_rows * n_cols
NUM_STEPS = 25
KILL_RATIO = .6

def convert_to_spectrogram(filename='./tmp/guess.wav'):
	png_file = filename[:-4] + '.png'
	return plot_spect(filename, png_file)

def record_and_eval(chord):
	frets = Guitar.read_chord(chord)
	start_recording_thread('./tmp/guess.wav')
	Guitar.play_chord(frets)
	time.sleep(1)
	return convert_to_spectrogram()

def draw_x():
	ax = plt.gca()
	patch = patches.Rectangle((1,1), 5.9, .75, color='k', angle=45)
	ax.add_patch(patch)
	patch = patches.Rectangle((1,5), 5.9, .75, color='k', angle=-45)
	ax.add_patch(patch)

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
	
	Guitar.openJVM()
	for i in range(MAX_POP_SIZE):
		chord = Chord()
		chord_pos[chord] = i+1
		pop.append(chord)
	print('Beginning natural selection with {} organisms'.format(len(pop)))
	# Repeat following for x number of steps:
	for step in range(NUM_STEPS):
		f.canvas.set_window_title('Step {}/{}'.format(step+1, NUM_STEPS))
		print('BEGINNING STEP NUMBER', step)
		for i in range(MAX_POP_SIZE):
			plt.subplot(n_rows, n_cols, i+1)
			pop[i].plot_chord()
			plt.title('Chord {}: f=unknown'.format(i+1))
		plt.pause(0.05)
		# **Calculate and assign fitness to each organism**
		# - Start recording
		# - play chord by guitar.py
		# - convert wav to spectrogram by plot_spectrogram.py
		# - fitness = MSE(target image, guess image)
		for c, chord in enumerate(pop):
			fitness = record_and_eval(chord)
			chord.fitness = fitness
			plt.subplot(n_rows,n_cols,c+1)
			plt.title('Chord {}: f={}'.format(c+1,round(fitness,2)))
			plt.pause(0.05)
		avg_f = np.mean([c.fitness for c in pop])
		print('Average fitness of step:', avg_f)
		avg_fitness.append(avg_f)
		# **Kill the weakest chords**
		# The bottom 50% or so of the population in terms of fitness
		# will be eliminated and will not have a chance to breed.
		# - sort by fitness
		# - remove the bottom half
		pop.sort(key=lambda x: (x.fitness), reverse=False)
		print([x.fitness for x in pop])
		for c, chord in enumerate(pop[int(len(pop)*KILL_RATIO):]):
			plt.subplot(n_rows, n_cols,chord_pos[chord])
			plt.title('Killed')
			draw_x()
			chord.alive = False
			print('Killed Chord {} with f={}'.format(chord_pos[chord],chord.fitness))
			pop.remove(chord)
			plt.pause(0.5)

		# **Breed the organisms to refill the population**
		# - Lowest fitness should breed the most
		# - Use chord_breeder.py to generate offspring
		candidates = np.copy(pop)
		[np.append(candidates,pop[0]) for _ in range(first_place_bonus)]
		[np.append(candidates,pop[1]) for _ in range(second_place_bonus)]
		[np.append(candidates,pop[2]) for _ in range(third_place_bonus)]
		candidates = np.repeat(candidates,3)
		candidates = np.random.permutation(candidates)

		print('Population size after deletion:',len(pop))
		diff = MAX_POP_SIZE - len(pop)
		print('Diff:',diff)
		i = 0
		while len(pop) < MAX_POP_SIZE:

			chord = chord_breeder.breed(candidates[i*2], candidates[i*2+1], debug=True)
			print('----------')
			pop.append(chord)

			chord_pos[chord] = find_empty_spot(chord_pos)
			i+=1

		print('Population size after breeding:',len(pop))
		plt.pause(1)
		plt.clf()
	plt.figure()
	plt.plot(avg_fitness)
	plt.show()
		
	Guitar.closeJVM()