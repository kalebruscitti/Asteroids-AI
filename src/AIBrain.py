import numpy as np
from asteroids import *
from ai import *
from soundManager import *
# number of games to play
trials = 2


class Brain():

	def __init__(self):
		self.score_array = np.empty([0, 1])

	def runAI(self):

		initSoundManager()
		game = Asteroids()
		game.playGame()
		score = game.sendScore()
		self.score_array = np.append(self.score_array, score)

	def runGeneration(self):
		for i in range(trials):
			self.AI = AI()
			Brain.runAI()
			weights = AI.sendWeights()
			print(" ")
			print(weights)
			print("^weights^")
			del self.AI
		print(Brain.score_array)

	def breed(self):
		score_array = self.score_array
		self.score_array = np.empty([0, 1])
		best_dex = np.argmax(score_array)
		print(best_dex)


Brain = Brain()
Brain.runGeneration()
Brain.breed()

#test
