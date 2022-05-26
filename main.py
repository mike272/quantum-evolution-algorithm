from Src.GUI.Visualization.quantum_flappy_cow import Game
from Src.settings import *
from Src.GUI.quantum_gui import QuantumGUI

settings = Settings(

    epochs = 20, 

    batch_size = 2048,                  
    
    model_name = 'quantum bits boi',             
    verbose = 1,
    print_summary = True  
)

game = Game()
game.play() 
#app = QuantumGUI(settings)
#app.run()