import numpy as np
from scipy.stats import linregress as linregress
from asteroids import *
from ai import *
from soundManager import *
#number of games to play when training
trials = 1

class Brain():

	def __init__(self):
		#store scores
		self.score_array = np.empty([0,1])
		self.weight_array = np.empty([0,1])
		self.bias_array = np.empty([0,5])
		self.readFile()

	def readFile(self):
		return None

	def runAI(self):
		#run one instance of the game
		initSoundManager()
		self.game = Asteroids()
		self.game.playGame()

	def linearRegression(self, scores, inputs):
		input_array = np.transpose(inputs)
		reg_array = np.empty([0,2])
		for i in input_array:
			m, b, r, p, err = linregress(scores,i)
			reg_array = np.append(reg_array, np.array([[m,b]]), 0)
		return reg_array

	def partialCost(self, m, b, a):
		y = (m*(50000-(m*a+b)))
		return y

	def sigmoidPrime(self, z):
		y = 1/(1+np.exp(z * -1)) - np.pow((1/(1+np.exp(z * -1))),2)
		return y

	def learn(self):
		score_m , input_m = self.game.sendMemory()
		reg_array =  self.linearRegression(score_m, input_m)

		for entry in reg_array:
			m, b = entry[0], entry[1]
			print(m, b)




Brain = Brain()
#repeat training
for i in range(trials):
	Brain.runAI()
	Brain.learn()


file = open("memory.txt", "w")
n = 0
for score in Brain.score_array:
	file.write(str(score) + " ")
	for bias in Brain.bias_array[n]:
		file.write(str(bias) + " ")
	file.write("\n")
	n += 1
file.close()
#test
