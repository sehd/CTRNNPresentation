from rnn import Rnn
from time import sleep
from math import *
from random import *
from multiprocessing import pool
import numpy as np

#Parameters
processCount = 8
populationSize = 128
breedingPoolSize = 32
hiddenLayerSize = 50
mutationChance = 0.01

#Prepare next generation
def Breed(parrents:list):
    Wxh = np.zeros((4,hiddenLayerSize))
    Whh = np.zeros((hiddenLayerSize,hiddenLayerSize))
    Why = np.zeros((hiddenLayerSize,3))
    bh = np.zeros(hiddenLayerSize)
    by = np.zeros(3)

    parrentChance = (1 - mutationChance) / 2
    selectionChances = [parrentChance,parrentChance,mutationChance]
    #Crossover
    for x in range(0,4):
        for y in range(0,hiddenLayerSize):
            parrentWxh = list(parrent[0]['Wxh'][x][y] for parrent in parrents)
            parrentWxh.append(np.random.normal())
            Wxh[x][y] = choices(parrentWxh,selectionChances)[0]

    for x in range(0,hiddenLayerSize):
        for y in range(0,hiddenLayerSize):
            parrentWhh = list(parrent[0]['Whh'][x][y] for parrent in parrents)
            parrentWhh.append(np.random.normal())
            Whh[x][y] = choices(parrentWhh,selectionChances)[0]
        for y in range(0,3):
            parrentWhy = list(parrent[0]['Why'][x][y] for parrent in parrents)
            parrentWhy.append(np.random.normal())
            Why[x][y] = choices(parrentWhy,selectionChances)[0]

        parrentBh = list(parrent[0]['bh'][x] for parrent in parrents)
        parrentBh.append(np.random.normal())
        bh[x] = choices(parrentBh,selectionChances)[0]

    for x in range(0,3):
        parrentBy = list(parrent[0]['by'][x] for parrent in parrents)
        parrentBy.append(np.random.normal())
        by[x] = choices(parrentBy,selectionChances)[0]

    return (Wxh,Whh,Why,bh,by)

def ProcessGenerationPart(Weights):
    population = []
    for x in range(0,populationSize // processCount):
        rnn = Rnn(hiddenLayerSize)
        if(Weights[x][0] is not None):
            rnn.SetWeightsManually(Weights[x][0],Weights[x][1],Weights[x][2],Weights[x][3],Weights[x][4])
        rnn.start()
        population.append(rnn)
    sleep(60)
    for rnn in population:
        rnn.Stop()

    error = []
    for rnn in population:
        state = rnn.GetState()
        error.append(({'Wxh': rnn.Wxh,'Whh': rnn.Whh,'Why': rnn.Why,'bh': rnn.bh,'by': rnn.by,'State': rnn.GetState()},(state[0][0] - pi / 2) ** 2 + ((state[0][1] - pi / 2) / 2) ** 2 + (state[1][0] / 2) ** 2 + (state[1][1]) ** 2))
    return error

if __name__ == '__main__':
    p = pool.Pool(processCount)
    error = []
    res = p.map(ProcessGenerationPart,[[(None,None,None,None,None)] * (populationSize // processCount)] * processCount)
    p.close()
    for i in range(0,processCount):
        error+=res[i]
    
    for i in range(1,100):    
        error.sort(key=lambda err:err[1])
        print('Best of population ' + str(i) + ': Error = ' + str(error[0][1]) + ' Degrees = ' + str(error[0][0]['State'][0]))
        Best = str(error[0][0])
        print('Worst of population ' + str(i) + ': Error = ' + str(error[populationSize - 1][1]) + ' Degrees = ' + str(error[populationSize - 1][0]['State'][0]))
        #------------------------Should bail out if good enough
    
        successful_strains = error[0:breedingPoolSize]
        children = []
        for x in range(0,populationSize):
            parrents = choices(successful_strains,k=2)
            children.append(Breed(parrents))
        
        processSeparatedChildren = []
        threadPerProcessCount = populationSize // processCount
        for x in range(0,processCount):
            processSeparatedChildren.append(children[x * threadPerProcessCount:(x + 1) * threadPerProcessCount])
    
        p = pool.Pool(processCount)
        error = []
        res = p.map(ProcessGenerationPart,processSeparatedChildren)
        p.close()
        for i in range(0,processCount):
            error+=res[i]

    print("Best weights: " + Best)