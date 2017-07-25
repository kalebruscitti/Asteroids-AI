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
        self.neurons = 5
        #change this number to the number of neurons
        self.generateNeurons()

    def sendInput(self, baddie_array, ship_angle, ship_position):
        print("pos:")
        print(ship_position)
        self.input_array = np.array([False,False,False,False,False])
        n = 0
        left = 0
        for neuron in self.Neuron_array:
            out = neuron.output(baddie_array, ship_angle, ship_position)
            if out > 0.4:
                if n == 1:
                    left = out
                if n == 2:
                    if left >= out:
                        self.input_array[1] = True
                    else:
                        self.input_array[2] = False
                else:
                    self.input_array[n] = True
            n += 1
        return self.input_array

    def generateNeurons(self):
        self.Neuron_array = np.empty([0,1])
        for n in range(self.neurons):
            neuron = Neuron()
            self.Neuron_array = np.append(self.Neuron_array, neuron)

    def sendWeights(self):
        weights = np.empty([0,3])
        for neuron in self.Neuron_array:
            np.append(weights, neuron.weights_and_bias)
        return weights

class Neuron():
    def __init__(self):
        self.angle_weights = np.random.rand()
        self.pos_weights = np.random.rand(1, 2)
        self.baddie_weights = np.random.rand(1, 3)
        self.bias = 0
        self.weights_and_bias = np.array([self.angle_weights, self.pos_weights, self.baddie_weights, self.bias])

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    def output(self, baddie_array, ship_angle, ship_position):
        x = 0
        print(str(self.pos_weights) + "_pos_")
        x += np.dot(self.angle_weights, ship_angle)
        x += np.dot(self.pos_weights, ship_position)
        x -= self.bias
        print(str(x) + "_x_")
        print(str(self.sigmoid(x)) + "_sigmoid_")


        return self.sigmoid(x)
