from note import Note
import numpy as np
from jpype import startJVM, shutdownJVM, java, addClassPath, JClass, JInt
import jpype.imports
import matplotlib.pyplot as plt
from recorder import start_recording_thread
import time
class Guitar():
	jvm_open = False

	open_string_tunings = {
	 6: Note('E',2),
	 5: Note('A',2),
	 4: Note('D',3),
	 3: Note('G',3),
	 2: Note('B',3),
	 1: Note('E',4)
	}
	# Converts the finger shapes into something more readable
	@staticmethod
	def read_chord(chord):
		frets_list = np.zeros(6)
		current_fret = 0
		for f in chord.fingers:
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
		for c,i in enumerate(frets_list):
			notes_list.append(Note.decode_dist(Guitar.open_string_tunings[c+1].increment(i)))
		return np.flip(frets_list).astype(np.int16)

	@staticmethod
	def play_chord(chord):
		try:
			pass # Not sure why we need a pass here
			tester = JClass('SoundTester')
			#muter = tester.audioSource
			e_ = java.lang.Integer(chord[0]) # Unpacking the integers
			a = java.lang.Integer(chord[1]) # from the list to supply
			d = java.lang.Integer(chord[2]) # it in an easier fashion
			g = java.lang.Integer(chord[3]) # to the JVM
			b = java.lang.Integer(chord[4])
			e = java.lang.Integer(chord[5])
			tester.playChordTab(e_,a,d,g,b,e)
			time.sleep(2.5)
			#muter.clearOutChannels()
		except Exception as e:
			print(f"Exception: {e}")

	@staticmethod
	def openJVM():
		startJVM(convertStrings=False)
		jvm_open = True

	@staticmethod
	def closeJVM():
		shutdownJVM()
		jvm_open = False


if __name__ == '__main__':
	Guitar.openJVM()
	chord = Chord()
	
	notes, frets = Guitar.read_chord(chord)
	print([str(i) for i in notes])
	print([i for i in frets])
	chord.plot_chord()
	plt.show()
	start_recording_thread('./tmp/test.wav')
	Guitar.play_chord(frets)
	Guitar.closeJVM()
