from Src.GUI.Visualization.visualization import Game
from Src.settings import *
from Src.GUI.quantum_gui import QuantumGUI

settings = Settings()

#game = Game()
#game.play() 
app = QuantumGUI(settings)
app.run()