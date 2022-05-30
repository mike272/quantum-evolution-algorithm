from random import randint
from Src.GUI.Visualization.logic import randomMutatedBits, randomStartingBits
from Src.GUI.Visualization.visualization import Visualization
from Src.GUI.quantum_gui import QuantumGUI
from Src.settings import *
import pygame


"""
SIMULATION CONTROLS:

A - FPS lock toggle (limit to MAX_FPS const or max render speed possible, affects simulation in render mode only)
S - Rendering toggle (renders cows - low fps/stops rendering - huge pp fps)
X - Kills first player (in list)
ESC - Quit
"""

neurons = 1 # neurons - 1 on the first layer, 1 neuron output layer
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
    mutation_rate=0,                    #Note: 0 is auto (1/bits)
    leaders_count=8,
    neurons=neurons,
    float_precision=float_precision,    #Note: float precision of 5 means 4 float bits + 1 sign bit
    bits_count=10,                       #Note: 0 is auto (from eq above)
    silent=False,
    i_know_what_im_doing=True,           #No security assertions
    pipes=50,
    player_controlled=False,
    initial_bits="0",
)
 
#app = QuantumGUI(settings)

if(settings.initial_bits[0]!="1"):
    bits = randomStartingBits(settings)
else:
    bits = randomMutatedBits(settings)

mode = 1
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