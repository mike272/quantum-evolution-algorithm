from typing import List

from Src.const import INPUT_SHAPE

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
        mutation_rate = 0,  #auto   
        babies_count = 40,
        leaders_count = 5,
        bits_count = 0,     #auto
        initial_bits = "0",  
        float_precision = 5,             
        verbose = 1,
        neurons = 3,
        pipes = 100,

        players = [],
        silent = False,
        quantum = False,
        player_controlled = False,
        i_know_what_im_doing = False
    ):
        self.epochs = epochs  
        
        self.mutation_rate = mutation_rate
        self.babies_count = babies_count
        self.leaders_count = leaders_count
        self.bits_count = bits_count
        self.initial_bits = initial_bits
        self.float_precision = float_precision
        self.neurons = neurons
        self.pipes = pipes
        self.players = players
        self.silent = silent
        self.quantum = quantum
        self.player_controlled = player_controlled
        self.verbose = verbose

        if self.bits_count == 0:
            self.bits_count = self.float_precision*INPUT_SHAPE*2 if self.neurons==1 \
                else self.float_precision*(self.neurons-1)*(INPUT_SHAPE+1)
            print(f"AUTO bits_count: {self.bits_count}")

        print(f"BITS usage: {self.bits_count} total - {INPUT_SHAPE*self.float_precision} input - {self.bits_count - INPUT_SHAPE*self.float_precision} weights")


        if(self.mutation_rate <= 0 or self.mutation_rate>=1):
            self.mutation_rate = round(1/self.bits_count,2)
            print(f"AUTO mutation_rate: {self.mutation_rate}")


        if(len(self.initial_bits) != self.bits_count):
            self.initial_bits = (self.initial_bits*self.bits_count)[:self.bits_count]
            print(f"REPEAT initial_bits: {self.initial_bits}")

        if not i_know_what_im_doing:
            if self.neurons!=1:
                assert(self.float_precision*(self.neurons-1)*(INPUT_SHAPE+1)<=self.bits_count)
            else:
                assert(self.float_precision*INPUT_SHAPE*2<=self.bits_count)


