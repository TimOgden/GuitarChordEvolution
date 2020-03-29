class Note():
	dist_from_middle_c_dict = {'A': -3, 'A#': -2, 'B': -1, 'C': 0,
		'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
		'F#': 6, 'G': 7, 'G#': 8}
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

	@staticmethod
	def decode_dist(dist_from_middle_c):
		dist = dist_from_middle_c
		octave = dist_from_middle_c // 12 + 3
		key_list = list(Note.dist_from_middle_c_dict.keys())
		value_list = list(Note.dist_from_middle_c_dict.values())
		try:
			letter = key_list[value_list.index(dist_from_middle_c % 12)]
		except:
			letter = key_list[value_list.index(dist_from_middle_c % -12)]
			octave += 1
		return Note(letter, octave)

	def increment(self, dist):
		dist_from_middle_c = self.dist_from_middle_c()
		return (dist_from_middle_c+dist)

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