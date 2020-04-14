import numpy as np
class LinearInterpolation:
	def __init__(self, start, end, end_step):
		self.start = start
		self.end = end
		self.end_step = end_step

	def interpolate(self, step):
		val = self.start*(1-step/self.end_step) + self.end*(step/self.end_step)
		return np.clip(val, self.start, self.end)