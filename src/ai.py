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
        #also go to the outputNeuron class and change the number there
        self.neurons=8
        self.output_layer = self.generateNeurons(5, False)
        self.hidden_layer = self.generateNeurons(self.neurons, True)
        self.current_score = 0
        self.score_memory = np.empty([0,1])
        self.input_memory = np.empty([0,5])

    def sendInput(self, baddie_array, ship_angle, ship_position, score):
        #reset the inputs from the last cycle
        self.input_array = np.array([False,False, False,False,False])
        output_array = self.feedForward(baddie_array, ship_angle, ship_position)
        final_array = np.empty([0,5])
        n = 0 #counter
        left = 0
        for neuron in self.output_layer:
            out = neuron.output(output_array)
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
            final_array = np.append(final_array, out)
        self.storeData(score, np.array([final_array]))
        return self.input_array

    def feedForward(self, baddie_array, ship_angle, ship_position):
        output_array = np.array([[]])
        for neuron in self.hidden_layer:
            out = neuron.output(baddie_array, ship_angle, ship_position)
            output_array = np.array([np.append(output_array, out)])
        return output_array

    def generateNeurons(self, neurons, hidden):
        Neuron_array = np.empty([0,1])
        #neuron array allows us to iterate over them easily
        if hidden:
            for n in range(neurons):
                neuron = hiddenNeuron()
                Neuron_array = np.append(Neuron_array, neuron)
        else:
            for n in range(neurons):
                neuron = outputNeuron()
                Neuron_array = np.append(Neuron_array, neuron)

        return Neuron_array

    def sendBias(self):
        #save array, send and delete it
        send_bias_array = self.bias_array
        self.bias_array = np.empty([0,1])
        return send_bias_array

    def reinit(self):
        #bool array where each index corresponds to a possible action.
        self.input_array = np.array([False,False,False,False,False])
        self.current_score = 0
        self.score_memory = np.empty([0,1])
        self.input_memory = np.empty([0,5])
        for neuron in self.output_layer:
            adj = np.random.rand(1,)
            neuron.adjust(adj)
            self.bias_array = np.append(self.bias_array, neuron.bias)
        #return memory to the Brain

    def storeData(self, score, input_array):
        self.score_memory = np.append(self.score_memory, score)
        self.input_memory = np.append(self.input_memory, input_array, 0)

    def sendMemory(self):
        return self.score_memory, self.input_memory

class hiddenNeuron(): #sigmoid neuron
    def __init__(self):
        ##To do: recieve calculated inputs using gradient descent
        self.angle_weights = np.random.rand()
        self.pos_weights = np.random.rand(1,2)
        self.baddie_weights = np.random.rand(2,)
        self.bias = np.random.rand(1,)

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
        #x is the "weighted input"
        return self.sigmoid(self.x)

    def adjust(self, adj):
        self.bias += adj

class outputNeuron():
    def __init__(self):
        ##change this if you change AI.neurons above.
        self.inputs = 8
        self.weights = np.random.rand(self.inputs,)
        self.biases = np.random.rand(1,)

    def sigmoid(self, x):
        return 1/(1 + np.exp(x)) #sigma(x) where x = (w dot I - b)

    def output(self, inputs):
        z = np.dot(inputs, self.weights)
        z -= self.biases
        z *= -1
        return self.sigmoid(z)
