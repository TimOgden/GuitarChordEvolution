import random
import matplotlib.pyplot as plt
from finger_technique import *
import abc
class Finger():
	def __init__(self, increment=None, start_fret=None, technique=None, 
			string=None, stop_string=None, dist_covered=0):
		self.increment = increment
		if increment is None:
			self.increment = random.randint(0,4-dist_covered)
		self.start_fret = start_fret
		if start_fret is None:
			self.start_fret = random.randint(1,20)
		self.technique = technique
		if technique is None:
			self.technique = random.choice(Technique.possibilities)
		self.string = string
		if string is None:
			self.string = random.randint(1,6)
		self.stop_string = stop_string
		if stop_string is None:
			self.stop_string = random.randint(1, self.string)

