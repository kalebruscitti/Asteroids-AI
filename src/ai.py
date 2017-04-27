import numpy as np
from asteroids import *
# Machine Learning AI for Asteroids
# This AI is designed to work with a modified version of Pythonic Asteroids (see "original readme.txt")
# by Kaleb Ruscitti (kaleb.ruscitti.ca) 
 
class AI():
	def __init__(self): 
		self.input_array = np.array([False,False,False,False,False])
		#bool array for each action
		self.p_array = np.random.random_sample((5,))
		#probability array for each action
		return None
	def thrust(self):
		self.input_array[0] = True

	def turnLeft(self):
		self.input_array[1] = True 

	def turnRight(self):
		self.input_array[2] = True
	
	def sendInput(self,baddie_array):
		self.input_array = np.array([False,False,False,False,False])
		#randomly generate 5 values
 		self.random_array = np.random.random_sample((5,))
		#execute the actions statistically
		n = 0
		for value in self.p_array:
			if value > self.random_array[n]:
				self.input_array[n] = True
			n += 1 
		return self.input_array	
	
