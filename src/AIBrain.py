import numpy as np
from asteroids import *
from ai import *
from soundManager import *
#number of games to play
trials = 2

class Brain():

	def __init__(self):
		self.score_array = np.empty([0,1])

	def runAI(self):

		initSoundManager()
		game = Asteroids()
		game.playGame()
		score = game.sendScore()
		self.score_array = np.append(self.score_array, score)

AI = AI()
Brain = Brain()
for i in range(trials):
	Brain.runAI()

print(Brain.score_array)
