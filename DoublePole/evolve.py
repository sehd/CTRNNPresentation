from rnn import Rnn
from time import sleep
from math import *
from random import *
import numpy as np

#Parameters
populationSize = 100
breedingPoolSize = 30
hiddenLayerSize = 50

#Initiation
population = []
for x in range(0,populationSize):
    print("Starting thread " + str(x + 1))
    rnn = Rnn(hiddenLayerSize)
    rnn.start()
    population.append(rnn)
    
for i in range(1,100):

    #Run the population
    print("Waiting for population to run")
    sleep(6)
    
    for rnn in population:
        rnn.Stop()
    
    error = []
    for rnn in population:
        state = rnn.GetState()
        error.append((rnn,(state[0][0] - pi / 2) ** 2 + ((state[0][1] - pi / 2) / 2) ** 2 + (state[1][0] / 2) ** 2 + (state[1][1]) ** 2))
    
    error.sort(key=lambda err:err[1])
    print('Best of population ' + str(i) + ': Error = ' + str(error[0][1]) + ' Degrees = ' + str(error[0][0].GetState()[0]))
    print('Worst of population ' + str(i) + ': Error = ' + str(error[populationSize - 1][1]) + ' Degrees = ' + str(error[populationSize - 1][0].GetState()[0]))
    #------------------------Should bail out if good enough
    
    #Prepare next generation
    def Breed(parrents:list):
        Wxh = np.zeros((4,hiddenLayerSize))
        Whh = np.zeros((hiddenLayerSize,hiddenLayerSize))
        Why = np.zeros((hiddenLayerSize,3))
        bh = np.zeros(hiddenLayerSize)
        by = np.zeros(3)

        #Crossover
        for x in range(0,4):
            for y in range(0,hiddenLayerSize):
                parrentWxh = tuple(parrent[0].Wxh[x][y] for parrent in parrents)
                Wxh[x][y] = choice(parrentWxh)

        for x in range(0,hiddenLayerSize):
            for y in range(0,hiddenLayerSize):
                Whh[x][y] = choice(tuple(parrent[0].Whh[x][y] for parrent in parrents))
            for y in range(0,3):
                Why[x][y] = choice(tuple(parrent[0].Why[x][y] for parrent in parrents))
            bh[x] = choice(tuple(parrent[0].bh[x] for parrent in parrents))

        for x in range(0,3):
            by[x] = choice(tuple(parrent[0].by[x] for parrent in parrents))

        #Mutation
        #TODO

        return (Wxh,Whh,Why,bh,by)

    successful_strains = error[0:breedingPoolSize]
    population.clear()
    for x in range(0,populationSize):
        parrents = choices(successful_strains,k=2)
        child = Breed(parrents)
        print("Starting thread " + str(x + 1))
        rnn = Rnn(hiddenLayerSize)
        rnn.SetWeightsManually(child[0],child[1],child[2],child[3],child[4])
        rnn.start()
        population.append(rnn)