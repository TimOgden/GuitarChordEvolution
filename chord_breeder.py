import numpy as np
from chord import Chord
from guitar import Guitar
import random
from finger_technique import Technique
from finger import Finger
import matplotlib.pyplot as plt
MUTATION_RATE = .3


def set_mutation_rate(mutation_rate):
	MUTATION_RATE = mutation_rate

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
				if debug:
					print('Finger was added through mutation')
				return Finger()
		return None
	if mutate():
		if debug:
			print("Finger {} was mutated".format(c+1))
		return Finger()
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
		if mutate():
			i+=1 # Skip finger i (this means that the child will have one less finger)
		if i>=len(a.fingers):
			a_finger = None
		else:
			a_finger = a.fingers[i]
		if i>=len(b.fingers):
			b_finger = None
		else:
			b_finger = b.fingers[i]
		desired_finger = combine_2(a_finger, b_finger,i, debug=debug)
		if desired_finger is not None:
			fingers.append(desired_finger)
	c = Chord(fingers=fingers)
	
	
	if debug:
		print('Chord {} bred with Chord {}'.format(a.subplot, b.subplot))
	return c

#if __name__ == '__main__':

