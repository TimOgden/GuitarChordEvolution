import random
import matplotlib.pyplot as plt
from finger_technique import *
import abc
class Finger():
	def __init__(self, fret=None, technique=None, string=None, stop_string=1):
		if fret is None:
			self.randomize()
		else:
			self.fret = fret
			self.technique = technique
			self.string = string
			self.stop_string = stop_string

	def __str__(self):
		return str('Finger on string {}, fret {}, {}'.format(self.string, self.fret,
				 self.technique))

	@abc.abstractmethod
	def randomize(self):
		pass
	

class FirstFinger(Finger):
	def __init__(self, fret=None, technique=None, string=None, stop_string=1):
		super(FirstFinger, self).__init__(fret, technique, string,stop_string)


	def randomize(self):
		self.fret = random.randint(0, 20)
		self.technique = random.choice(Technique.possibilities)
		self.string = random.randint(1,6)
		self.stop_string = random.randint(1,self.string)

class AdditionalFinger(Finger):
	def __init__(self, fret=None, technique=None, string=None, stop_string=1):
		super(AdditionalFinger,self).__init__(fret,technique,string,stop_string)


	def randomize(self):
		self.fret = random.randint(0, 3)
		self.technique = random.choice(Technique.possibilities)
		self.string = random.randint(1,6)
		self.stop_string = random.randint(1,self.string)