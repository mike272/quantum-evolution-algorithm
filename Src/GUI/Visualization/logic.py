from random import random, randint
import numpy as np

from typing import List
from Src.settings import Settings
from Src.GUI.Visualization.logic_cpu import *
from Src.GUI.Visualization.logic_quantum import *


class Layer:
    def __init__(self, weights:np.ndarray|List[FloatQubit]):
        self.size = len(weights)
        self.weights = weights

    def multiply(self, input:np.ndarray) -> float:
        return multiply(input, self.weights)

    def multiplyQ(self, input:List[FloatQubit]) -> FloatQubit:
        return multiplyQ(input, self.weights)
        
def randomStartingBits(settings:Settings):
    bits = []
    for i in range(0,settings.babies_count):
        x = randint(2**39, 2**40-1)
        b = format(x,'b').zfill(settings.bits_count)
        bits.append(b)
    return bits

def randomBits(s:str, m:float):
    o = ""

    for i in range(0, len(s)):
        if(random()<m):
            if(s[i] == "0"):
                o+="1"
            else:
                o += "0"
        else:
            o+=s[i]

    return o   

def initializeNetwork(bits:str, settings:Settings) -> List[Layer]:

    network:List[Layer]

    if(settings.quantum):
        l1, offset = createNFloatsQ(bits,3, settings.float_precision) 
        l2, offset = createNFloatsQ(bits,3, settings.float_precision, offset) 
        l3, offset = createNFloatsQ(bits,2, settings.float_precision, offset)
        network = [Layer(l1),Layer(l2),Layer(l3)]
    else:
        l1, offset = createNFloats(bits,3, settings.float_precision) 
        l2, offset = createNFloats(bits,3, settings.float_precision, offset) 
        l3, offset = createNFloats(bits,2, settings.float_precision, offset) 
        network = [Layer(l1),Layer(l2),Layer(l3)]

    return network

def processBits(input:List[float], layers:List[Layer], quantum:bool = False) -> bool:
    if quantum:
        input = preprocessInputQ(input)
        layer0_1_output = layers[0].multiplyQ(input)
        layer0_2_output = layers[1].multiplyQ(input)

        layer0_output = [layer0_1_output, layer0_2_output]

        layer1_output = layers[2].multiplyQ(layer0_output)

        return mapQ(layer1_output)

    else:
        input = preprocessInput(input)
        layer0_1_output = layers[0].multiply(input)
        layer0_2_output = layers[1].multiply(input)

        layer0_output = np.array([layer0_1_output, layer0_2_output])

        layer0_output = np.reshape(layer0_output, (2))

        layer1_output = layers[2].multiply(layer0_output)

        return map(layer1_output)
        

