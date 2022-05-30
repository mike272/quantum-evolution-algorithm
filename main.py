from random import randint
from Src.GUI.Visualization.logic import randomStartingBits
from Src.GUI.Visualization.visualization import Visualization
from Src.GUI.quantum_gui import QuantumGUI
from Src.settings import *
import pygame

neurons = 1 #neurons - 1 on the first layer, 1 neuron output layer
float_precision = 5

'''
The eq for bits FOR WEIGHTS is as follows:
FOR NEURONS != 1:
    float_precision*(INPUT_SHAPE*(neurons-1) + neurons - 1) = float_precision*(neurons-1)*(INPUT_SHAPE+1)
FOR NEURONS == 1:
    float_precision*INPUT_SHAPE

TOTAL, WITH INPUTS:
N!=1:    
    float_precision*((neurons-1)*(INPUT_SHAPE+1)+INPUT_SHAPE)
N==1:
    float_precision*INPUT_SHAPE*2

'''
settings = Settings(
    babies_count=100,
    mutation_rate=0, #Note: 0 is auto (1/bits)
    leaders_count=10,
    neurons=neurons,
    float_precision=float_precision, #Note: float precision of 5 means 4 float bits + 1 sign bit
    bits_count=float_precision*INPUT_SHAPE*2 if neurons==1 else float_precision*(neurons-1)*(INPUT_SHAPE+1)
)
 
#app = QuantumGUI(settings)
#app.run()

mode = 1

bits = randomStartingBits(settings)
if(mode==0):
    try:
        game = Visualization(bits, settings)
        game.play()
    except Exception as e:
        print("======= ERR =======")
        print(e)
        pygame.quit()
else:
    game = Visualization(bits, settings)
    game.play()