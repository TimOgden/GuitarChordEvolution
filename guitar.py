from note import Note
from chord import Chord
import numpy as np
class Guitar():
	open_string_tunings = {
	 6: Note('E',2),
	 5: Note('A',2),
	 4: Note('D',3),
	 3: Note('G',3),
	 2: Note('B',3),
	 1: Note('E',4)
	}

	@staticmethod
	def read_chord(chord):
		frets_list = np.zeros(6)
		current_fret = 1
		for f in chord.fingers:
			current_fret += f.fret
			if(f.technique=='Full_Barre' or f.technique=='Partial_Barre'):
				for s in range(f.stop_string, f.string+1):
					frets_list[s-1] = current_fret
			if(f.technique=='Single_Note_Then_Mute'):
				frets_list[f.string-1] = current_fret
				for i in range(f.stop_string-1, f.string):
					frets_list[i-1] = -9999
			if(f.technique=='Single_Note_Then_Open'):
				frets_list[f.string-1] = current_fret
		notes_list = []
		for c,i in enumerate(frets_list):
			notes_list.append(Note.decode_dist(Guitar.open_string_tunings[c+1].increment(i)))
		return notes_list, frets_list

	@staticmethod
	def play_chord(chord):
		notes, frets = read_chord(chord)
		

if __name__ == '__main__':
	chord = Chord()
	
	notes, frets = Guitar.read_chord(chord)
	print([str(i) for i in notes])
	print([int(i) for i in frets])
	chord.plot_chord()
