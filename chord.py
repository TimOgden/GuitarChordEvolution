import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from finger import FirstFinger, AdditionalFinger
class Chord(object):
	FRETBOARD_SIZE = 7
	FINGER_COLORS = ['b','r','g','c']
	def __init__(self):
		self.fingers = []
		self.fingers.append(FirstFinger())
		self.start_fret = self.fingers[0].fret
		self.fitness = float('inf')
		self.alive = True
		for i in range(np.random.randint(0,4)):
			self.fingers.append(AdditionalFinger())

	def plot_chord(self):
		#plt.figure(figsize=(6,7))
		start_fret = self.fingers[0].fret
		end_fret = start_fret + self.FRETBOARD_SIZE
		x_axis = np.arange(start_fret,end_fret)
		y_axis = np.arange(1,7)
		
		ax = plt.gca()
		#plt.plot(x_axis, y_axis)

		#[fret_dict[k] = i for i,k in zip(np.arange(.5,4.5),np.flip(np.arange(start_fret,end_fret,step=1)))]
		plt.yticks(np.arange(.5,self.FRETBOARD_SIZE + .5),
			np.flip(np.arange(start_fret,end_fret,step=1))) # Labeling the frets
		plt.xticks(np.arange(6),np.flip(np.arange(1,7,step=1))) # Labeling the strings, may remove later
		
		# Adding lines to draw strings
		[plt.axvline(x=i,color='k', linewidth=(6-i)/2) for i in np.arange(0,6)]
		# Adding lines to draw frets
		[plt.axhline(y=i,color='k') for i in np.arange(end_fret-start_fret)]
		current_fret = 1
		c = 0
		for f in self.fingers:
			current_fret += f.fret
			#print("Current fret:", current_fret)
			patch = self.plot_finger(f, current_fret, c)
			c+=1
			if(patch):
				ax.add_patch(patch)
		#rect = patches.Rectangle((.5,0.125), 1, .75)
		#ax.add_patch(rect)
		#plt.axes()

	def plot_finger(self, finger, current_fret, c):
		bl_x = 5 - finger.string + .5
		bl_y = self.FRETBOARD_SIZE - 1 - (current_fret - self.start_fret) + .125
		width = .9
		if(finger.technique=='Full_Barre'):
			width = (finger.string+1)*.9
		if(finger.technique=='Partial_Barre'):
			width = (finger.string-finger.stop_string+1)*.9
		rect = patches.Rectangle((bl_x,bl_y), width, .75, color=self.FINGER_COLORS[c])
		#print("Plotting finger at string:{}, fret:{} with technique:{}".format(finger.string,current_fret
		#				,finger.technique))
		return rect

		

if __name__ == "__main__":
	n_rows, n_cols = 5,5
	for i in range(n_rows*n_cols):
		plt.subplot(n_rows, n_cols, i+1)
		chord = Chord()
		chord.plot_chord()
	plt.show()