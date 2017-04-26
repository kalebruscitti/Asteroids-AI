import numpy as np

# AI for Asteroids
# Start with testing the ability to input 
 
class AI():
	def __init__(self): 
		self.input_array = np.array([False,False,False,False,False])
		 #Bool array to store which inputs are active
		return None
	def thrust(self):
		self.input_array[0] = True

	def turnLeft(self):
		self.input_array[1] = True 

	def turnRight(self):
		self.input_array[2] = True
	
	def sendInput(self):
		self.determinAction()
		return self.input_array
	
	def determineAction(self):	
