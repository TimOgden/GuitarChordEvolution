import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from finger import Finger
class Chord(object):
	FRETBOARD_SIZE = 7
	FINGER_COLORS = ['b','r','g','c']
	def __init__(self, fingers=None):
		dist_covered = 0
		if fingers is None:
			self.fingers = []
			for i in range(np.random.randint(1,5)):
				finger = Finger(dist_covered=dist_covered)
				self.fingers.append(finger)
				if i != 0:
					dist_covered += finger.increment
		else:
			self.fingers = fingers
		if len(self.fingers) > 0:
			self.start_fret = self.fingers[0].start_fret
		else:
			self.start_fret = 0
		self.fitness = float('inf')
		self.alive = True
		self.subplot = None
		
	def make_frets_readable(self, frets):
		frets = frets.astype(str)
		#print(frets)
		np.place(frets, frets=='0', 'o')
		np.place(frets, frets=='-9999', 'x')
		return frets
	
	def read(self):
		frets_list = np.zeros(6)
		current_fret = 0
		
		for c, f in enumerate(self.fingers):
			if c == 0:
				current_fret += f.start_fret
			else:
				current_fret += f.increment
			if(f.technique=='Barre'):
				for s in range(f.stop_string, f.string+1):
					frets_list[s-1] = current_fret

			if(f.technique=='Barre_Mute_Above'):
				if f.string != 6:
					frets_list[f.string] = -9999
				for s in range(f.stop_string, f.string+1):
					frets_list[s-1] = current_fret

			if(f.technique=='Single_Note_Then_Mute'):
				frets_list[f.string-1] = current_fret
				for i in range(f.stop_string, f.string):
					frets_list[i-1] = -9999

			if(f.technique=='Single_Note'):
				frets_list[f.string-1] = current_fret

			if(f.technique=='Single_Note_Mute_Above'):
				if f.string != 6:
					frets_list[f.string] = -9999
				frets_list[f.string-1] = current_fret

			if(f.technique=='Mute'):
				for i in range(f.stop_string, f.string+1):
					frets_list[i-1] = -9999


		return np.flip(frets_list).astype(np.int16)

	def plot(self, debug=False):
		#plt.figure(figsize=(6,7))
		start_fret = self.start_fret
		if debug:
			print('start fret is {}'.format(start_fret))
		end_fret = start_fret + self.FRETBOARD_SIZE
		
		ax = plt.gca()

		plt.yticks(np.arange(.5,self.FRETBOARD_SIZE + 1.5),
			np.flip(np.arange(start_fret-1,end_fret,step=1))) # Labeling the frets
		plt.xticks(np.arange(6),self.make_frets_readable(self.read()))
		
		# Adding lines to draw strings
		[plt.axvline(x=i,color='k', linewidth=(6-i)/2) for i in np.arange(0,6)]
		# Adding lines to draw frets
		[plt.axhline(y=i,color='k') for i in np.arange(end_fret-start_fret+1)]
		current_fret = 0
		for c, f in enumerate(self.fingers):
			if c == 0:
				current_fret += f.start_fret
			else:
				current_fret += f.increment
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
		alpha = 1
		if(finger.technique=='Barre' or finger.technique=='Barre_Mute_Above'
			or finger.technique=='Mute'):
			width = (finger.string-finger.stop_string+1)*.9
		if finger.technique=='Mute':
			alpha = .3
		rect = patches.Rectangle((bl_x,bl_y), width, .75, color=self.FINGER_COLORS[c], alpha=alpha)
		if debug:
			print('Plotting finger {} at y {}'.format(c+1,bl_y))
		#print("Plotting finger at string:{}, fret:{} with technique:{}".format(finger.string,current_fret
		#				,finger.technique))
		return rect

