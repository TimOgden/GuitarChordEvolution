# GuitarChordEvolution
Uses an evolutionary algorithm to generate guitar chords with no knowledge of music theory.

## Installation

```git clone https://github.com/TimOgden/GuitarChordEvolution```

```pip install -r requirements.txt```

**Note:** If you are on windows, the installation of PyAudio is likely to fail. Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio, find the appropriate version for your version of python and put it in your working directory. Then call ```pip install [YOUR .WHL FILE]```.

## How to use

In evolution.py, you can set RUNS at the top to a number higher than 1 if you want to run the simulation multiple times, but you usually want to keep it at 1.

In the main method, you can define each finger how you wish and then pass up to 4 fingers into the master_chord:

```
# Defining master chord (this example is an open C chord)
	f1 = Finger(string=2, technique='Single_Note', start_fret=1)
	f2 = Finger(string=4, technique='Single_Note', increment=1)
	f3 = Finger(string=5, technique='Single_Note_Mute_Above', increment=1)
	#f4 = Finger(string=1, technique='Single_Note', increment=3)
	master_chord = Chord(fingers=[f1,f2,f3])
```

Now run with ```python evolution.py```. The best population will be saved in ```best.pickle``` before closing.

To evaluate the best population, run ```python examine_pickle.py```.
