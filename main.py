from random import randint
from Src.GUI.Visualization.logic import randomStartingBits
from Src.GUI.Visualization.visualization import Visualization
from Src.settings import *
from Src.GUI.quantum_gui import QuantumGUI

settings = Settings(
    babies_count=60,
    mutation_rate=0.1

)

game = Visualization(randomStartingBits(settings), settings)
game.play() 
#app = QuantumGUI(settings)
#app.run()
