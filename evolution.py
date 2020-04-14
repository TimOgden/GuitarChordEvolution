import numpy as np
from chord import Chord
from guitar import Guitar
from finger import Finger
from note import Note
import matplotlib.pyplot as plt
from misc_tools import TwoWayDict
from linearinterpolation import LinearInterpolation
import chord_breeder
import matplotlib.patches as patches
import pickle

n_rows, n_cols = 4,9
first_place_bonus = 2 # How many more chances does 1st, 2nd, 3rd place get
second_place_bonus = 1 # to breed?
third_place_bonus = 0
INCORRECT_NUMBER_NOTES_PENALTY = 1
MAX_POP_SIZE = n_rows * n_cols
NUM_STEPS = 50 # How many iterations of killing/breeding should take place; if -1, go until terminated
START_KILL_RATIO = .3
KILL_RATIO_LIMIT = .6
kill_ratio_max = 25 # At what step should the kill ratio hit the limit
KILL_PAUSE, FITNESS_PAUSE = .2, .5 # Controls the speed of matplotlib
patience = 3 # How many steps does there have to be a decrease in avg fitness for evolution to end

pop = []
fitnesses = []
interpolations = {}
master_frequencies = None
chord_pos = {}
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

def find_empty_spot():
	for chord in chord_pos.values():
		if type(chord) != Chord:
			continue
		if not chord.alive:
			return chord_pos[chord]
	return None

def patient():
	if len(fitnesses)<patience+1:
		return True
	for i in range(patience):
		if fitnesses[-patience+i-1] > fitnesses[-patience+i]:
			return True
	return False

def fitness_eval(frequencies):
	matrix = []
	#print('Master:',master_frequencies)
	#print('Other:',frequencies)
	for r, freq in enumerate(master_frequencies):
		row = []
		for c, m_freq in enumerate(frequencies):
			#print(m_freq, freq)
			row.append(abs(Note.num_half_steps(m_freq, freq)))
		matrix.append(row)
	matrix = np.array(matrix)
	col_mins = [None, None] # Placeholder to satisfy the first iteration of while loop
	delta = 0
	while len(col_mins) > 1:
		col_mins = np.amin(matrix, axis=0)[:len(frequencies)]
		smallest_col = np.argmin(col_mins) # This freq achieves (with some m_freq) the closest step count
		
		#print('Matrix:')
		#print(matrix)

		#print('Column mins:',col_mins)
		#print('---------------')
		# Now that we know which m_freq has the potential to be the closest,
		# let's find the freq/m_freq combo that is closest
		desired_row = np.argmin(matrix[:,smallest_col])
		delta += matrix[desired_row,smallest_col]
		#print('Desired row:',desired_row, 'Desired col:',smallest_col, 'Delta:',delta)
		matrix = np.delete(matrix, smallest_col, axis=1)
	if len(frequencies) < len(master_frequencies):
		#print('Number of frequencies does not match')
		return delta + (len(master_frequencies) - len(frequencies))*INCORRECT_NUMBER_NOTES_PENALTY
	return delta

def evolution_step(step, save_best=False):
	f.canvas.set_window_title('Step {}/{}'.format(step+1, NUM_STEPS))
	print('BEGINNING STEP NUMBER', step)
	kill_ratio = interpolations['Kill Ratio'].interpolate(step)
	for i in range(MAX_POP_SIZE):
		plt.subplot(n_rows, n_cols, i+1)
		pop[i].plot()
		chord_pos[pop[i]] = i+1
		pop[i].subplot = i+1
		plt.title('Chord {}: f=unknown'.format(i+1))
	plt.pause(FITNESS_PAUSE)
	# **Calculate and assign fitness to each organism**
	# - Start recording
	# - play chord by guitar.py
	# - convert wav to spectrogram by plot_spectrogram.py
	# - fitness = MSE(target image, guess image)
	row = []
	for c, chord in enumerate(pop):
		#fitness = record_and_eval(chord)
		frequencies = Guitar.frequency_list(chord.read())
		fitness = fitness_eval(frequencies)
		#fitness = np.count_nonzero(np.isin(master_frequencies,frequencies)) + .5*np.count_nonzero(np.mod(frequencies,master_frequencies)==0)
		#cartesian_product = np.transpose([np.tile(frequencies,len(master_frequencies)), np.repeat(master_frequencies,len(frequencies))])
		
		#fitness = sum(np.absolute([Note.num_half_steps(f1,f2) for f1,f2 in cartesian_product]))/len(cartesian_product)
		chord.fitness = fitness
		plt.subplot(n_rows,n_cols,c+1)
		plt.title('Chord {}: f={}'.format(c+1,round(fitness,2)))
		row.append(fitness)
	plt.pause(FITNESS_PAUSE)
	avg_f = np.mean([c.fitness for c in pop])
	if save_best:
		if len(fitnesses) > 0:
			if avg_f < min(np.mean(fitnesses, axis=1)):
				with open('best.pickle', 'wb') as file:
					pickle.dump(pop, file)
	fitnesses.append(row)
	# **Kill the weakest chords**
	# The bottom 50% or so of the population in terms of fitness
	# will be eliminated and will not have a chance to breed.
	# - sort by fitness
	# - remove the bottom half
	pop.sort(key=lambda x: (x.fitness), reverse=False)
	for c, chord in enumerate(pop[-1:int(len(pop)*(1-kill_ratio)):-1]):
		plt.subplot(n_rows, n_cols,chord_pos[chord])
		plt.title('Killed')
		draw_x()
		chord.alive = False
		print('Killed Chord {} with f={}'.format(chord_pos[chord],chord.fitness))
		pop.remove(chord)
	plt.pause(KILL_PAUSE)

	# **Breed the organisms to refill the population**
	# - Lowest fitness should breed the most
	# - Use chord_breeder.py to generate offspring
	candidates = np.copy(pop)
	[np.append(candidates,pop[0]) for _ in range(first_place_bonus)]
	[np.append(candidates,pop[1]) for _ in range(second_place_bonus)]
	[np.append(candidates,pop[2]) for _ in range(third_place_bonus)]
	candidates = np.repeat(candidates,4)
	candidates = np.random.permutation(candidates)

	print('Population size after deletion:',len(pop))
	diff = MAX_POP_SIZE - len(pop)
	i = 0
	while len(pop) < MAX_POP_SIZE:
		chord_breeder.set_mutation_rate(interpolations['Mutation Rate'].interpolate(step))
		offspring_a = chord_breeder.breed(candidates[i*2], candidates[i*2+1], debug=False)
		offspring_b = chord_breeder.breed(candidates[i*2], candidates[i*2+1], debug=False)
		print('----------')
		pop.append(offspring_a)
		chord_pos[offspring_a] = find_empty_spot()
		if(len(pop)< MAX_POP_SIZE):
			pop.append(offspring_b)
			chord_pos[offspring_b] = find_empty_spot()
		
		i+=1

	print('Population size after breeding:',len(pop))
	plt.pause(KILL_PAUSE)
	

if __name__ == "__main__":
	# Defining master chord
	f1 = Finger(string=2, technique='Single_Note', start_fret=1)
	f2 = Finger(string=4, technique='Single_Note', increment=1)
	f3 = Finger(string=5, technique='Single_Note_Mute_Above', increment=1)
	#f4 = Finger(string=5, technique='Single_Note', increment=0)
	master_chord = Chord(fingers=[f1,f2,f3])
	master_frequencies = Guitar.frequency_list(master_chord.read())

	print('Master frequencies:',master_frequencies)
	master_chord.plot()
	plt.title('Master Chord')
	plt.show()
	# Initializing the population randomly
	f, axs = plt.subplots(n_rows, n_cols, sharex=True)
	#f.tight_layout(pad=1.0)
	chord_pos = TwoWayDict()
	
	mng = plt.get_current_fig_manager()
	mng.window.state('zoomed')
	kill_interp = LinearInterpolation(start=.3,end=.6,end_step=25)
	mutation_interp = LinearInterpolation(start=.1,end=.4,end_step=50)
	interpolations['Kill Ratio'] = kill_interp
	interpolations['Mutation Rate'] = mutation_interp
	for i in range(MAX_POP_SIZE):
		chord = Chord()
		pop.append(chord)
	print('Beginning natural selection with {} organisms'.format(len(pop)))
	if NUM_STEPS!=-1:
		# Repeat following for x number of steps:
		for step in range(NUM_STEPS):
			plt.clf()
			evolution_step(step, save_best=True)
			
	else:
		step = 0
		while patient():
			plt.clf()
			evolution_step(step, save_best=True)
			step+=1

	fitnesses = np.array(fitnesses)
	plt.figure()
	plt.subplot(2,1,1)
	plt.title('Average fitness at each step')
	plt.plot(np.mean(fitnesses, axis=1))
	plt.subplot(2,1,2)
	plt.title('Minimum fitness at each step')
	plt.plot(np.amin(fitnesses, axis=1))
	plt.show()