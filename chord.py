import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from finger import FirstFinger, AdditionalFinger
class Chord(object):
	FRETBOARD_SIZE = 7
	FINGER_COLORS = ['b','r','g','c']
	def __init__(self, fingers=None):
		if fingers is None:
			self.fingers = []
			self.fingers.append(FirstFinger())
			for i in range(np.random.randint(0,4)):
				self.fingers.append(AdditionalFinger())
		else:
			self.fingers = fingers
		self.start_fret = self.fingers[0].fret
		self.fitness = float('inf')
		self.alive = True
		self.subplot = None
		
	def make_frets_readable(self, frets):
		frets = frets.astype(str)
		#print(frets)
		np.place(frets, frets=='0', 'o')
		np.place(frets, frets=='-9999', 'x')
		return frets
	
	def read_chord(self):
		frets_list = np.zeros(6)
		current_fret = 0
		
		for f in self.fingers:
			current_fret += f.fret
			if(f.technique=='Full_Barre'):
				for s in range(1, f.string+1):
					frets_list[s-1] = current_fret
			if(f.technique=='Partial_Barre'):
				for s in range(f.stop_string, f.string+1):
					frets_list[s-1] = current_fret
			if(f.technique=='Single_Note_Then_Mute'):
				frets_list[f.string-1] = current_fret
				for i in range(f.stop_string, f.string):
					frets_list[i-1] = -9999
			if(f.technique=='Single_Note'):
				frets_list[f.string-1] = current_fret
		notes_list = []
		return np.flip(frets_list).astype(np.int16)

	def plot_chord(self, debug=False):
		#plt.figure(figsize=(6,7))
		start_fret = self.fingers[0].fret
		if debug:
			print('start fret is {}'.format(start_fret))
		end_fret = start_fret + self.FRETBOARD_SIZE
		
		ax = plt.gca()

		plt.yticks(np.arange(.5,self.FRETBOARD_SIZE + 1.5),
			np.flip(np.arange(start_fret-1,end_fret,step=1))) # Labeling the frets
		plt.xticks(np.arange(6),self.make_frets_readable(self.read_chord()))
		
		# Adding lines to draw strings
		[plt.axvline(x=i,color='k', linewidth=(6-i)/2) for i in np.arange(0,6)]
		# Adding lines to draw frets
		[plt.axhline(y=i,color='k') for i in np.arange(end_fret-start_fret+1)]
		current_fret = 0
		c = 0
		for f in self.fingers:
			current_fret += f.fret
			#print("Current fret:", current_fret)
			patch = self.plot_finger(f, current_fret, c, debug=debug)
			c+=1
			if(patch):
				ax.add_patch(patch)
		#rect = patches.Rectangle((.5,0.125), 1, .75)
		#ax.add_patch(rect)
		#plt.axes()

	def plot_finger(self, finger, current_fret, c, debug=False):
		bl_x = 5 - finger.string + .5
		bl_y = self.FRETBOARD_SIZE - 1 - (current_fret - self.start_fret) + .125
		width = .9
		if(finger.technique=='Full_Barre'):
			width = (finger.string+1)*.9
		if(finger.technique=='Partial_Barre'):
			width = (finger.string-finger.stop_string+1)*.9
		rect = patches.Rectangle((bl_x,bl_y), width, .75, color=self.FINGER_COLORS[c])
		if debug:
			print('Plotting finger {} at y {}'.format(c+1,bl_y))
		#print("Plotting finger at string:{}, fret:{} with technique:{}".format(finger.string,current_fret
		#				,finger.technique))
		return rect

