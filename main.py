from Src.loader import *
from Src.categorizer import *
from Src.settings import *
from Src.GUI.classifier_gui import ClassifierGUI

# =================
# ALEXNET MODEL
# VERSION MINI/BASIC
# ==================

settings = ModelSettings(
    # Defines how many convolutional layers in the network, and how many filters per layer.
    # len(convolution_layers) is how many layers are in a network.
    # After every layer, MaxPool2D is performed (exluding the last one).
    # A layer size can be a single integer, or an array of integers
    # If it is an array, there are multiple Conv2Ds before MaxPool2D
    # It is a good idea to use a numer which is a power of 2
    convolution_layers = [              
                [16,16],                
                [32,32],
                [64,64]
    ],

    # Activation to be used in the filters
    # Either 'relu', 'tanh'. 
    # Relu is much faster but the loss function might explode upwards                           
    convolution_activation = ActivationType.relu,

    # Defines filter sizes per layer.
    # Len of this array must match convolution_layers'
    # Only integers are allowed!!! + make sure it is an ODD number
    # Filter of size n is n x n matrix
    convolution_sizes = [               
                3,
                3,
                3
    ],      

    # Defines the layer that connects Conv layers with Dense layers
    # Either 'global_avg', 'maxpool','flatten'
    # global_avg is significantly faster but might lose some information 
    # maxpool is a jack of all trades
    # flatten is the best but slow as turtle
    middle_layer = MiddleLayerType.max_pool,

    # Defines how many dense layers in the network, and the neuron count.
    # len(dense_layers) is how many layers are in a network.
    # After every layer, Dropout is performed is performed (exluding the last one).
    # A layer size can be a single integer, or an array of integers
    # It is a good idea to use a numer which is a power of 2
    # Works similarly to Conv2D in that regard
    dense_layers = [                    
                1024,
                1024
    ],

    # Activation to be used in the neurons
    # Either 'relu', 'tanh'. 
    # Relu is much faster but the loss function might explode upwards            
    dense_activation = ActivationType.relu,          

    # Chance of deactivating the output of any neuron
    # It is a number between 0 and 1
    # Prevents overfitting with higher values, but harder to learn
    dropout_rate = 0.2,

    # Optimizer to be used in the network, from the following:
    # 'SGD' (momentum gradient descent),     
    # 'RMSprop' (decaying learning rate), 
    # 'adam' (both basically)
    # It is almost always a good idea to use adam
    optimizer = OptimizerType.adam,                 

    # How fast the network is learning (Speed of gradient descent)
    # Higher values make it much easier to learn at first, good for testing
    # But it is harder then to achieve decent accuracy in the long-term
    # Value between 0.0 - 0.01
    learning_rate = 0.001,              

    # How many epochs to perform
    epochs = 20, 

    # This value determines how many steps there are in a single epoch
    # Increases training time, but helps with overfitting
    # data_count/batch_size is the number of steps
    # If batch_size = 1, it is called a stochastic gradient descent
    # Which is extremely good for learning
    # But you can go asleep before a single epoch finishes
    # Also, reducing this may help memory errors, as less images are loaded into memory
    batch_size = 2048,                  
    

    # Optional, not really important
    model_name = 'alexy',               # Name of the model
    validation_split = 0.1,             # Percentage of data used for validation of learning outcomes            
    verbose = 1,                        # Either 1 (on) or 0 (off)
    print_summary = True                # Prints network summary upon creation
)

app = ClassifierGUI(settings)
#app.run()

'''
# Creates Graphs, Models folders if missing
create_required_files_and_folders_if_missing()

# Main code requires preprocessing to finish succesfully
verify_preprocessing_complete()

# Load features and labels datasets into memory with selected features
images, labels, breeds_count = load_images_labels()

# Creates the model with specified structure and properties
model = create_model(
    breeds_count = breeds_count,
    settings = settings
)

# Compiles the model and prints its summary
model = compile_model(
    model = model,
    settings = settings
)

# Trains the model over given amoount of epochs, tests data on validation dataset
model, history = train_model(
    model = model,
    images = images,
    labels = labels,
    settings = settings
)

# Saves the accuracy & loss graphs, saves statistics to the CSV file
model_name, graph_name = save_statistics(
    history = history,
    settings = settings
)

# Saves graphs that display accuracy and loss
save_graph(
    history = history,
    graph_name = graph_name,
    settings = settings
)

# Saves model into the folder with name specified below (adds unique id to the file name)
save_model(
    model = model,
    model_name = model_name
)
'''