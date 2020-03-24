import random
import matplotlib.pyplot as plt
from finger_technique import *
class Finger():
	def __init__(self, fret=0, technique='Single_Note_Then_Open', string=6, stop_string=1):
		self.fret = fret
		self.technique = technique
		self.string = string
		self.stop_string = stop_string

	def randomize(self):
		pass



	def __init__(self):
		self.randomize()

	

class FirstFinger(Finger):
	def __init__(self):
		super(FirstFinger, self).__init__()

	def randomize(self):
		self.fret = random.randint(0, 20)
		self.technique = random.choice(Technique.possibilities)
		self.string = random.randint(1,6)
		self.stop_string = random.randint(1,self.string)

class AdditionalFinger(Finger):
	def __init__(self):
		super(AdditionalFinger, self).__init__()

	def randomize(self):
		self.fret = random.randint(0, 3)
		self.technique = random.choice(Technique.possibilities)
		self.string = random.randint(1,6)
		self.stop_string = random.randint(1,self.string)