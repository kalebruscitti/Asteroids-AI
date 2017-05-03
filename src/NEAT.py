'''
NEAT Neural Network to play Asteroids, an old Arcade Game.

Acknoledgements to Nick Redshaw for his Pythenic Asteroids (2008)
which this program uses as an engine for the Asteroids game.

The program uses the NEAT (neuro-evolution of augmenting topologies)
methodology to evolve a neural network which can play Asteroids at a level
similar to a human.

By Kaleb Ruscitti and Joshua Varga (2017)
'''

import numpy as np
from soundManager import *
from asteroids import *
from ai import *
'Parameters'
children_per_generation = c_g = 3
generations = gens = 2
number_of_hidden_neurons = n_h = 8


def main():
    for i in range(gens):
        if i == 0:
            genes = 0
        print("Generation: " + str(i))
        genes, max_fit = runGeneration(genes)
        print("Maximum fitness: " + str(max_fit))


def runChild(genes):
    initSoundManager()
    game = Asteroids(0)
    game.playGame()
    score = game.sendScore()
    o_bias, h_bias = game.collectWnB()
    return score, np.array([o_bias]), np.array([h_bias])


def runGeneration(genes):
    '#first we run all of the children'
    scores = np.empty([0, 1])
    o_biases = np.empty([0, 5])
    h_biases = np.empty([0, n_h])
    for i in range(c_g):
        score, o_bias, h_bias = runChild(genes)
        scores = np.append(scores, score)
        o_biases = np.append(o_biases, o_bias, 0)
        h_biases = np.append(h_biases, h_bias, 0)
    '#now we select the best 2 results for breeding'
    alphas = np.empty([0, 1])
    for i in range(2):
        index = np.argmax(scores)
        if i == 0:
            max_fit = scores[index]
        scores[index] = 0
        alphas = np.append(alphas, np.array([index]))

    alphas_o_biases = np.empty([0, 5])
    alphas_h_biases = np.empty([0, n_h])
    for i in alphas:
        i = int(i)
        h_biases[i] = h_bias
        o_biases[i] = o_bias
        alphas_o_biases = np.append(alphas_o_biases, o_bias, 0)
        alphas_h_biases = np.append(alphas_h_biases, h_bias, 0)
    '#we have two arrays with the "genes" of the breeding pair'
    '#so we can send that to breed the next generation'
    chromosome = breed(alphas_h_biases, alphas_o_biases)
    return chromosome, max_fit


def breed(h_biases, o_biases):
    '#we randomly select the father or mother\'s gene with 50/50 chance'
    o_genes = np.array([])
    h_genes = np.array([])
    for n in range(5):
        x = np.random.choice(o_biases[:, n])
        o_genes = np.append(o_genes, x)
    for n in range(n_h):
        x = np.random.choice(h_biases[:, n])
        h_genes = np.append(h_genes, x)
    '#next we zip the genes into a chromosome'
    chromosome = np.array([o_genes, h_genes])
    return chromosome


main()
