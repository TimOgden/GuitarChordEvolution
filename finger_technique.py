class Technique():
	possibilities = ['Barre', 'Single_Note', 'Single_Note_Then_Mute', 'Single_Note_Mute_Above',
			'Barre_Mute_Above', 'Mute']
	def __init__(self):
		stop_string = 1 # Only applies to partial barre and single note then mute