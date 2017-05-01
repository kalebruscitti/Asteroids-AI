import numpy as np
from asteroids import *
from ai import *
from soundManager import *
#number of games to play when training
trials = 2

class Brain():

	def __init__(self):
		#store scores
		self.score_array = np.empty([0,1])
		self.weight_array = np.empty([0,1])
		self.bias_array = np.empty([0,5])

	def runAI(self,i):
		#run one instance of the game
		initSoundManager()
		game = Asteroids()
		game.playGame()
		score = game.sendScore()
		bias = np.array([AI.sendBias()])
		print("Bias: " + str(bias))
		AI.reinit()
		self.score_array = np.append(self.score_array, score)
		self.bias_array = np.append(self.bias_array, bias, 0)
		print("bias array \n" + str(self.bias_array))



Brain = Brain()
AI = AI()
#repeat training
for i in range(trials):
	Brain.runAI(i)


file = open("memory.txt", "w")
n = 0
for score in Brain.score_array:
	file.write(str(score) + " ")
	for bias in Brain.bias_array[n]:
		print(bias)
		file.write(str(bias) + " ")
	file.write("\n")
	n += 1
file.close()
#test
