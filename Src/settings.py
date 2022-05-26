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

    def __init__(self,
                                            
        epochs = 30, 
        mutation_rate = 0, # auto   
        babies_count = 100,
        leaders_count = 10,
        bits_count = 32,
        initial_bits = "00000000000000000000000000000000",  
        float_precision = 4,             
        verbose = 1
    ):
        self.epochs = epochs  
        
        self.mutation_rate = mutation_rate
        self.babies_count = babies_count
        self.leaders_count = leaders_count
        self.bits_count = bits_count
        self.initial_bits = initial_bits
        self.float_precision = float_precision

        if(mutation_rate == 0):
            self.mutation_rate = round(1/bits_count,2)
        
        self.verbose = verbose

        assert(len(self.initial_bits) == self.bits_count)

        if DEBUG: 
            self.epochs = 1
            self.verbose = 1

