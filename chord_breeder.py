import numpy as np
from chord import Chord
from guitar import Guitar
import random
from finger_technique import Technique
from finger import FirstFinger, AdditionalFinger, Finger
import matplotlib.pyplot as plt
MUTATION_RATE = .05

def combine_3(a_choice, b_choice, mutation):
	if np.random.uniform() < MUTATION_RATE:
		return mutation
	if np.random.uniform() < .5:
		return a_choice
	return b_choice

def combine_2(choice, mutation):
	if mutate():
		return mutation
	return choice

def mutate():
	return np.random.uniform() < MUTATION_RATE

def breed(a,b, debug=False):
	c = Chord()
	c.fingers = []
	c.alive = True
	for i in range(4):
		# new finger is a finger, b finger or dne
		finger = None
		if(i==0):
			finger = FirstFinger()
		else:
			finger = AdditionalFinger()
		a_exists = True
		b_exists = True
		if(i>=len(a.fingers)):
			a_exists = False
		if(i>=len(b.fingers)):
			b_exists = False

		if(a_exists and b_exists):
			if i == 0:
				finger.fret = combine_3(a.fingers[0].fret,b.fingers[0].fret, random.randint(0, 20))
			else:
				finger.fret = combine_3(a.fingers[i].fret,b.fingers[i].fret, random.randint(0,3))
			finger.technique = combine_3(a.fingers[i].technique,b.fingers[i].technique, random.choice(Technique.possibilities))
			finger.string = combine_3(a.fingers[i].string,b.fingers[i].string, random.randint(1,6))
			finger.stop_string = combine_3(a.fingers[i].stop_string,b.fingers[i].stop_string, random.randint(1,finger.string))
		if(a_exists and not b_exists):
			if i == 0:
				finger.fret = combine_2(a.fingers[0].fret, random.randint(0, 20))
			else:
				finger.fret = combine_2(a.fingers[i].fret, random.randint(0,3))
			finger.technique = combine_2(a.fingers[i].technique, random.choice(Technique.possibilities))
			finger.string = combine_2(a.fingers[i].string, random.randint(1,6))
			finger.stop_string = combine_2(a.fingers[i].stop_string, random.randint(1,finger.string))
		if(not a_exists and b_exists):
			if i == 0:
				finger.fret = combine_2(b.fingers[0].fret, random.randint(0, 20))
			else:
				finger.fret = combine_2(b.fingers[i].fret, random.randint(0,3))
			finger.technique = combine_2(b.fingers[i].technique, random.choice(Technique.possibilities))
			finger.string = combine_2(b.fingers[i].string, random.randint(1,6))
			finger.stop_string = combine_2(b.fingers[i].stop_string, random.randint(1,finger.string))
		else:
			# If mutation, finger.randomize(), else, finger is None
			finger = None
		if(finger):
			c.fingers.append(finger)
	if debug:
		_, frets_a = Guitar.read_chord(a)
		_, frets_b = Guitar.read_chord(b)
		_, frets_c = Guitar.read_chord(c)
		print('A:', [i for i in frets_a])
		print('B:', [i for i in frets_b])
		print('C:', [i for i in frets_c])

	return c

if __name__ == '__main__':
	a = Chord()
	b = Chord()
	plt.subplot(2,1,1)
	a.plot_chord()
	plt.subplot(2,1,2)
	b.plot_chord()
	plt.show()

	c = breed(a,b)
	c.plot_chord()
	plt.show()