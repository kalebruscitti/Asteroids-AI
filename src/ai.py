import numpy as np
from asteroids import *
# Machine Learning AI for Asteroids
# This AI is designed to work with a modified version of Pythonic Asteroids (see "original readme.txt") - Original Author: Nick Redshaw
# by Kaleb Ruscitti (kaleb.ruscitti.ca) and Joshua Varga

class AI():
    def __init__(self):
        #bool array where each index corresponds to a possible action.
        self.input_array = np.array([False,False,False,False,False])

        #change this number to the number of neurons in the first layer
        self.neurons=5
        self.generateNeurons()

    def sendInput(self, baddie_array, ship_angle, ship_position):
        #reset the inputs from the last cycle
        self.input_array = np.array([False,False, False,False,False])
        n = 0 #counter
        left = 0
        for neuron in self.Neuron_array:
            out = neuron.output(baddie_array, ship_angle, ship_position)
            #out is the value of \sigma(w dot I - b)
            if out > 0.5:
                #this if tree is required to choose between turning left or right
                #whichever of the two actions is higher is performed.
                if n == 1:
                    left = out
                if n == 2:
                    if left >= out:
                        self.input_array[1] = True
                    else:
                        self.input_array[2] = True
                else:
                    self.input_array[n] = True
            n += 1
        return self.input_array

    def generateNeurons(self):
        self.Neuron_array = np.empty([0,1])
        #neuron array allows us to iterate over them easily
        for n in range(self.neurons):
            neuron = Neuron()
            self.Neuron_array = np.append(self.Neuron_array, neuron)

class Neuron(): #sigmoid neuron
    def __init__(self):
        ##To do: recieve calculated inputs using gradient descent
        self.angle_weights = np.random.rand()
        self.pos_weights = np.random.rand(1,2)
        self.baddie_weights = np.random.rand(2,)
        self.bias = 0.75

    def sigmoid(self, x):
        return 1/(1 + np.exp(x)) #sigma(x) where x = (w dot I - b)


    def output(self, baddie_array, ship_angle, ship_position):
        #function calculates x = (w dot I - b) and sends it to the sigmoid function
        #w = weights, I = inputs, b = bias
        self.x = 0
        self.x += np.dot(self.angle_weights,ship_angle)
        self.x += np.dot(self.pos_weights, ship_position)
        for rock in baddie_array:
            self.x += np.dot(rock, self.baddie_weights)
        self.x -= self.bias
        self.x *= -1
        return self.sigmoid(self.x)
