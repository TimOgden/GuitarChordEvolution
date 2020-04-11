class Note():
	dist_from_middle_c_dict = {'A': -3, 'A#': -2, 'B': -1, 'C': 0,
		'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
		'F#': 6, 'G': 7, 'G#': 8}
	dist_from_a4_dict = {'A': 0, 'A#': 1, 'B': 2, 'C':3, 'C#': 4, 'D': 5, 'D#': 6,
	'E': 7, 'F': 8, 'F#': 9, 'G': 10, 'G#': 11}
	def __init__(self, note):
		self.letter = note[0]
		self.octave = note[1]

	def __init__(self, letter, octave):
		self.letter = letter
		self.octave = octave

	def dist_from_middle_c(self):
		middle_c = Note('C',3)
		octave_diff = middle_c.octave - self.octave
		return Note.dist_from_middle_c_dict[self.letter] - 12 * octave_diff

	def dist_from_a4(self):
		middle_a = Note('A',4)
		octave_diff = middle_a.octave - self.octave
		return Note.dist_from_a4_dict[self.letter] - 12 * octave_diff

	@staticmethod
	def decode_dist(dist_from_a4):
		dist = dist_from_a4
		octave = dist_from_a4 // 12 + 4
		key_list = list(Note.dist_from_a4_dict.keys())
		value_list = list(Note.dist_from_a4_dict.values())
		try:
			letter = key_list[value_list.index(dist_from_a4 % 12)]
		except:
			letter = key_list[value_list.index(dist_from_a4 % -12)]
			octave += 1
		return Note(letter, octave)

	@staticmethod
	def from_frequency(frequency):
		return decode_dist(int(12*np.log2(frequency/440)))

	def increment(self, dist):
		dist_from_a4 = self.dist_from_a4()
		return self.decode_dist(dist_from_a4+dist)

	def frequency(self):
		return 2**(self.dist_from_a4()/12)*440

	def __str__(self):
		if(self.dist_from_middle_c()<=-1000):
			return 'Muted'
		return self.letter + '_' + str(int(self.octave))

if __name__ == '__main__':
	#note = Note('A',2)
	#dist = note.dist_from_middle_c()
	#print(dist)
	#print("The note that is {} distance away from middle c is {}".format(dist, Note.decode_dist(dist)))
	note = Note('E',2)
	print(Note.decode_dist(note.increment(4)))