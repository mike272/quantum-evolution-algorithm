from Src.const import DEBUG
from enum import Enum

class ActivationType(Enum):
    relu = 1
    tanh = 2

class MiddleLayerType(Enum):
    flatten = 1
    max_pool = 2
    average_pool = 3

class OptimizerType(Enum):
    adam = 1
    SGD = 2
    RMSProp = 3

class ModelSettings:
    '''
    This class acts as a storage for model parameters.
    '''
    convolution_layers: list              
    convolution_activation: ActivationType
    convolution_sizes: list                   
    middle_layer: MiddleLayerType
    dense_layers: list
    dense_activation: ActivationType
    dropout_rate: float
    optimizer: OptimizerType
    learning_rate: float           
    epochs: int            
    batch_size: int                
    validation_split: float
    model_name: str
    print_summary: bool
    verbose: int

    def __init__(self,
        convolution_layers = [              
                    (32,32), 
                    (64,64),
                    (128,128)
        ],                              
        convolution_activation = 'relu',  
        convolution_sizes = [                
                    3,
                    3,
                    3
        ],                                 
        middle_layer = 'global_avg',        
        dense_layers = [                   
                    512, 
                    512, 
                    512
        ],              
        dense_activation = 'relu',          
        dropout_rate = 0.2,                 
        optimizer = 'adam',#                                     
        learning_rate = 0.001,#              
        epochs = 30,#                     
        batch_size = 2048,                
        validation_split = 0.1,#        
        model_name = 'model',#
        print_summary = True,#
        verbose = 1#
    ):
        self.convolution_layers = convolution_layers              
        self.convolution_activation = convolution_activation
        self.convolution_sizes = convolution_sizes   
        self.middle_layer = middle_layer
        self.dense_layers = dense_layers
        self.dense_activation = dense_activation
        self.dropout_rate = dropout_rate
        self.optimizer = optimizer
        self.learning_rate = learning_rate     
        self.epochs = epochs  
        self.batch_size = batch_size           
        self.validation_split = validation_split
        self.model_name = model_name
        self.print_summary = print_summary
        self.verbose = verbose

        assert(len(convolution_layers) == len(convolution_sizes))

        if DEBUG: 
            self.epochs = 1
            self.verbose = 1

    def __str__(self) -> str:
        if self.dense_activation == ActivationType.relu:
            dense_act = 'relu'
        elif self.dense_activation == ActivationType.tanh:
            dense_act = 'tanh'

        if self.convolution_activation == ActivationType.relu:
            conv_act = 'relu'
        elif self.convolution_activation == ActivationType.tanh:
            conv_act = 'tanh'

        if self.middle_layer == MiddleLayerType.average_pool:
            mlt = 'avg_pool'
        elif self.middle_layer == MiddleLayerType.max_pool:
            mlt = 'max_pool'
        elif self.middle_layer == MiddleLayerType.flatten:
            mlt = 'flatten'

        if self.optimizer == OptimizerType.adam:
            opt = 'adam'
        elif self.optimizer == OptimizerType.RMSProp:
            opt = 'RMSProp'
        elif self.optimizer == OptimizerType.SGD:
            opt = 'SGD'

        return ";".join([
                str(self.convolution_layers),              
                conv_act,
                str(self.convolution_sizes),  
                mlt,
                str(self.dense_layers),
                dense_act,
                str(self.dropout_rate),
                opt,
                str(self.learning_rate), 
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
    