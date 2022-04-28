from Src.const import DEBUG

class Settings:
    '''
    This class acts as a storage for model parameters.
    '''
          
    epochs: int            
    batch_size: int                
    validation_split: float
    model_name: str
    print_summary: bool
    verbose: int
    mutation_rate: int
    babies_count: int
    leaders_count: int
    bits_count: int
    initial_bits: int
    display_best: bool

    def __init__(self,
                                            
        epochs = 30,                   
        batch_size = 2048,                
        validation_split = 0.1,       
        model_name = 'model',
        print_summary = True,
        verbose = 1
    ):

        self.mutation_rate = 0.05
        self.babies_count = 100
        self.leaders_count = 10
        self.initial_bits_count = 12
        self.initial_bits = "000000000000"
        
        self.epochs = epochs  
        self.batch_size = batch_size           
        self.validation_split = validation_split
        self.model_name = model_name
        self.print_summary = print_summary
        self.verbose = verbose

        assert(len(self.initial_bits) == self.initial_bits_count)

        if DEBUG: 
            self.epochs = 1
            self.verbose = 1

    def __str__(self) -> str:
        

        return ";".join([
                str(self.epochs), 
                str(self.batch_size),
                "\n"
        ])

    @staticmethod
    def get_statistics_header_as_string():
        return ";".join([
            "Convolution layers",              
            "Convolution activation",
            "Convolution sizes",  
            "Middle layer",
            "Dense layers",
            "Dense activation",
            "Dropout rate",
            "Optimizer",
            "Learning rate", 
            "Epochs", 
            "Batch size",
            "\n"
        ])
    