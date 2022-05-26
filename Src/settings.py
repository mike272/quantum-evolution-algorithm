from typing import List

from numpy import quantile
from Src.const import DEBUG

class Settings:
    '''
    This class acts as a storage for model parameters.
    '''
          
    epochs: int            
    mutation_rate: float
    babies_count: int
    leaders_count: int
    bits_count: int
    initial_bits: int
    verbose: int

    players: List[str]
    silent: bool
    quantum: bool

    def __init__(self,
                                            
        epochs = 30, 
        mutation_rate = 0, # auto   
        babies_count = 40,
        leaders_count = 5,
        bits_count = 40,
        initial_bits = "0",  
        float_precision = 5,             
        verbose = 1,

        players = [],
        silent = False,
        quantum = False,
        player_controlled = False
    ):
        self.epochs = epochs  
        
        self.mutation_rate = mutation_rate
        self.babies_count = babies_count
        self.leaders_count = leaders_count
        self.bits_count = bits_count
        self.initial_bits = initial_bits
        self.float_precision = float_precision

        self.players = players
        self.silent = silent
        self.quantum = quantum
        self.player_controlled = player_controlled

        if(mutation_rate <= 0):
            self.mutation_rate = round(1/bits_count,2)
        
        self.verbose = verbose

        if(len(self.initial_bits) != self.bits_count):
            self.initial_bits = (self.initial_bits*self.bits_count)[:self.bits_count]


                                #3+3+2 architecture
        assert(self.float_precision*8<=self.bits_count)

        if DEBUG: 
            self.epochs = 1

