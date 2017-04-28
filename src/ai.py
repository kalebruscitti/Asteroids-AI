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
        self.neurons=5
        #change this number to the number of neurons
        self.generateNeurons()

    def sendInput(self, baddie_array, ship_angle, ship_position):
        print("pos:")
        print(ship_position)
        self.input_array = np.array([False,False,False,False,False])
        n = 0
        for neuron in self.Neuron_array:
            out = neuron.output(baddie_array, ship_angle, ship_position)
            if out > 0.5:
                self.input_array[n] = True
        return self.input_array

    def generateNeurons(self):
        self.Neuron_array = np.empty([0,1])
        for n in range(self.neurons):
            neuron = Neuron()
            self.Neuron_array = np.append(self.Neuron_array, neuron)

class Neuron():
    def __init__(self):
        self.angle_weights = np.random.randn(1,1)
        self.pos_weights = np.random.randn(1,2)
        self.baddie_weights = np.random.randn(1,2)
        self.bias = np.random.randn(1,2)

    def sigmoid(self, x):
        return 1/(1 + np.exp(x))

    def output(self, baddie_array, ship_angle, ship_position):
        self.main_data = np.array([[ship_angle, self.angle_weights], [ship_position, self.pos_weights]])

        for baddie in baddie_array:
            pos = np.array([[baddie[0],baddie[1]],[self.baddie_weights]])
            self.main_data = np.append(self.main_data, pos)


        x = 0
        for index in self.main_data:
            x += np.dot(index[0],index[1])
            x += self.bias

        return self.sigmoid(x)
