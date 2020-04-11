import numpy as np
from chord import Chord
from guitar import Guitar
import random
from finger_technique import Technique
from finger import FirstFinger, AdditionalFinger, Finger
import matplotlib.pyplot as plt
MUTATION_RATE = .1

def combine_2(a_finger, b_finger, c, debug=False):
	# Create new finger (in case of mutation)
	# If neither exist:
	#	If mutation:
	#		return mutation
	# If both exist:
	#	flip coin and return one of them
	# If a exists:
	#	return a
	# Else:
	#	return b
	#print(a_finger,b_finger)
	if a_finger is None and b_finger is None:
		if mutate():
				if c==0:
					if debug:
						print('First finger was added through mutation.')
					return FirstFinger(fret=None)
				else:
					if c < 3:
						if debug:
							print('Additional finger was added through mutation.')
						return AdditionalFinger(fret=None)
		return None
	if mutate():
		if debug:
			print("Finger {} was mutated".format(c+1))
		if c==0:
			return FirstFinger(fret=None)
		else:
			return AdditionalFinger(fret=None)
	if a_finger is not None and b_finger is not None:
		if np.random.uniform() < .5:
			if debug:
				print("Finger {} was selected from A".format(c+1))
			return a_finger
		else:
			if debug:
				print("Finger {} was selected from B".format(c+1))
			return b_finger
	if a_finger is not None:
		if debug:
			print("Finger {} was selected from A".format(c+1))
		return a_finger
	if debug:
		print("Finger {} was selected from B".format(c+1))
	return b_finger

def mutate():
	return np.random.uniform() < MUTATION_RATE

def breed(a,b, debug=False):
	fingers = []
	for i in range(4):
		if i>=len(a.fingers):
			a_finger = None
		else:
			a_finger = a.fingers[i]
		if i>=len(b.fingers):
			b_finger = None
		else:
			b_finger = b.fingers[i]
		desired_finger = combine_2(a_finger, b_finger,i, debug=True)
		if desired_finger is not None:
			fingers.append(desired_finger)
	c = Chord(fingers=fingers)
	
	
	if debug:
		print('A:',Guitar.read_chord(a))
		print('B:',Guitar.read_chord(b))
		print('C:',Guitar.read_chord(c))
	return c

if __name__ == '__main__':
	f1 = Finger(fret=1,technique='Single_Note',string=2)
	f2 = Finger(fret=1,technique='Single_Note',string=4)
	f3 = Finger(fret=1,technique='Single_Note',string=5)
	chord = Chord(fingers=[f1,f2,f3])
	frets = Guitar.read_chord(chord)
	frequencies = Guitar.frequency_list(frets)
	print(frequencies)
	chord.plot_chord()
	plt.show()
	#print([Note.from_frequency(frequencies)])
	
