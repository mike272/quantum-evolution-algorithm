from random import random, randint
from secrets import randbits
import numpy as np

from typing import List
from Src.const import INPUT_SHAPE
from Src.settings import Settings
from Src.GUI.Visualization.cow import Cow as Cow
from Src.GUI.Visualization.pipe import Pipe as Pipe
from Src.GUI.Visualization.logic_cpu import *
from Src.GUI.Visualization.logic_quantum import *
from Src.GUI.Visualization.layer import *


def initializeNetwork(bits:str, settings:Settings) -> List[Layer]:

    network:List[Layer] = [0]*settings.neurons

    createFloatsFunc = createNFloatsQ if settings.quantum else createNFloats

    offset = 0
    if settings.neurons!=1:
        for i in range(0, settings.neurons-1):
            l, offset = createFloatsFunc(bits, INPUT_SHAPE, settings.float_precision, offset)     
            network[i] = Layer(l)

        finalLayer, offset = createFloatsFunc(bits, settings.neurons-1, settings.float_precision, offset)
        network[settings.neurons-1] = Layer(finalLayer)
    else:
        l,offset = createFloatsFunc(bits, INPUT_SHAPE, settings.float_precision, offset)
        network[0] = Layer(l)

    return network

def processBits(input:List[float], layers:List[Layer], settings:Settings) -> bool:

    preprocFunc = preprocessInputQ if settings.quantum else preprocessInput
    multiplyFunc = multiplyQ if settings.quantum else multiply
    mapFunc = mapQ if settings.quantum else map

    input = preprocFunc(input, settings)
    if settings.neurons!=1:
        firstLayerOutput = [0]*(settings.neurons-1)

        for i in range(0, settings.neurons-1):
            firstLayerOutput[i] = multiplyFunc(input, layers[i].weights)

        firstLayerOutput = np.array(firstLayerOutput).reshape((settings.neurons-1)) if settings.quantum \
            else firstLayerOutput

        output = multiplyFunc(firstLayerOutput, layers[settings.neurons-1].weights)
    else:
        output = multiplyFunc(input, layers[0].weights)

    return mapFunc(output)
    
def randomStartingBits(settings:Settings):
    bits = [0]*settings.babies_count

    for i in range(0,settings.babies_count):
        b = randbits(settings.bits_count)
        bits[i] = format(b,'b').zfill(settings.bits_count)

    return bits

def randomMutatedBits(settings:Settings):
    bits = [0]*settings.babies_count

    bits[0] = settings.initial_bits
    for i in range(1, settings.babies_count):
        b = mutateBits(settings.initial_bits, settings.mutation_rate)
        bits[i] = b
    return bits

def makeCows(players:List[str],settings: Settings):
    cows = [0]*len(players)

    for i in range(0,len(players)):
        network = initializeNetwork(players[i], settings)
        cows[i] = Cow(network, players[i], settings, processBits)

    return cows

def makePipes(players:List[Cow], settings:Settings) -> List[Pipe]:
    pipes = [0]*settings.pipes

    for i in range(settings.pipes):
        pipes[i] = Pipe(PIPE_DIST*(i+1), players, settings)

    return pipes

def breed(players:List[Cow], settings: Settings) -> List[Cow]:
    champs = [p.bits for p in players[0:settings.leaders_count]]
    players = [0]*settings.babies_count

    for i in range(0, len(champs)):
        network = initializeNetwork(champs[i], settings)
        players[i] = Cow(network, champs[i], settings, processBits)
        players[i].makeRed()

    c = 0
    for i in range(len(champs), settings.babies_count):
        bits = mutateBits(champs[c%len(champs)], settings.mutation_rate)
        network = initializeNetwork(bits, settings)
        players[i] = Cow(network, bits, settings, processBits)
        c+=1

    return players 
