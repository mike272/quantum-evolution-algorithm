from typing import Tuple
import tensorflow as tf
import numpy as np
from time import time
import matplotlib.pyplot as plt
from tensorflow.keras import layers

from Src.const import *
from Src.settings import *

def create_model(breeds_count: int, settings: ModelSettings) -> tf.keras.models.Sequential :
    '''
    Creates a custom model based n input arguments.\n
    Model's structure: Input layer -> Reuqested Conv2Ds -> Middle layer -> Dense layers -> Output layer.\n
    Output layer is a Dense layer with softmax activation.
    '''
    model = tf.keras.Sequential()

    # Input layer
    model.add(layers.Input(shape=[IMAGE_SIZE, IMAGE_SIZE, 3]))

    if settings.convolution_activation == ActivationType.relu:
            convolution_activation = 'relu'
    elif settings.convolution_activation == ActivationType.tanh:
        convolution_activation = 'tanh'

    # Convolutional layers builder - Conv2D layer(s) followed by MaxPool2D. 
    for idx,layer in enumerate(settings.convolution_layers):
        s = settings.convolution_sizes[idx]

        if isinstance(layer, list) or isinstance(layer, tuple):
            for l in layer:
                model.add(layers.Conv2D(
                    filters = l,
                    kernel_size = (s, s), 
                    padding = 'same',
                    activation = convolution_activation
                ))
        else:
            model.add(layers.Conv2D(
                filters = layer,
                kernel_size = (s, s), 
                padding = 'same',
                activation = convolution_activation
            ))
        # Adds MaxPool2D after requested Conv2D layers
        # Does not add after the last layer, as some networks 
        # use different layer as a connector
        if idx < len(settings.convolution_layers) - 1:
            model.add(layers.MaxPool2D(
                pool_size = (2,2), 
                strides = (2,2)
            ))
        
    # Middle layer - connection between Conv2Ds and Dense
    # Flattens the shape from 4D to 2D
    if settings.middle_layer == MiddleLayerType.average_pool:
        model.add(layers.GlobalAveragePooling2D(
            data_format='channels_last'
        ))
    elif settings.middle_layer == MiddleLayerType.max_pool:
        model.add(layers.MaxPool2D(
            pool_size = (2,2), 
            strides = (2,2)
        ))
        model.add(layers.Flatten(
            data_format='channels_last'
        ))
    elif settings.middle_layer == MiddleLayerType.flatten:
        model.add(layers.Flatten(
            data_format='channels_last'
        ))

    
    if settings.dense_activation == ActivationType.relu:
        dense_activation = 'relu'
    elif settings.dense_activation == ActivationType.tanh:
        dense_activation = 'tanh'

    # Dense layers builder - Dense layer(s) followed by Dropout.
    for idx,layer in enumerate(settings.dense_layers):
        if isinstance(layer, list) or isinstance(layer, tuple):
            for l in layer:
                model.add(layers.Dense(
                    units = l,
                    activation = dense_activation
                ))
        else:
            model.add(layers.Dense(
                units = layer,
                activation = dense_activation
            ))
        # Adds dropout after adding requested dense layers
        model.add(layers.Dropout(
            rate = settings.dropout_rate
        ))
    
        
    # Output layer - dense layer that will output an array 
    # with breed predictions
    model.add(layers.Dense(
        breeds_count,
        activation='softmax'
    ))
    
    return model


def compile_model(model:tf.keras.Sequential, settings: ModelSettings) -> tf.keras.models.Sequential:
    '''
    Compiles the model with selected optimizer (adam/SGD/RMSProp) and learning rate.\n
    Uses 'accuracy' as a measure statistic, Categorical Cross Entropy loss function. 
    '''

    if(settings.optimizer==OptimizerType.adam):
        opt = tf.keras.optimizers.Adam(learning_rate=settings.learning_rate)
    elif(settings.optimizer==OptimizerType.SGD):
        opt = tf.keras.optimizers.SGD(learning_rate=settings.learning_rate)
    elif(settings.optimizer==OptimizerType.RMSProp):
        opt = tf.keras.optimizers.RMSprop(learning_rate=settings.learning_rate)

    model.compile(
        optimizer = opt,
        loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics = ['accuracy']
    )

    # Prints summary of the model, mostly for debug
    if settings.print_summary: model.summary()

    return model

def train_model(model:tf.keras.Sequential, 
                images:np.array, 
                labels:np.array, 
                settings: ModelSettings):
    '''
    Trains the model using provided images and labels.
    '''

    if(settings.verbose == 0): 
        print("[INFO] Training in progress...")

    history = model.fit(
        x = images,
        y = labels,
        validation_split=settings.validation_split,
        epochs=settings.epochs,
        batch_size=settings.batch_size,
        verbose=settings.verbose
    )

    return (model, history)

def save_statistics(history: tf.keras.callbacks.History, settings: ModelSettings):
    '''
    Loads training statistics from the model, and saves them to STATS_FILE.
    '''
    # Extract interesting statistics
    rounded_acc = round(history.history['val_accuracy'][-1],3)
    rounded_loss = round(history.history['val_loss'][-1],3)

    id = str(time())
    # Generate names for the model and object
    model_name = MODELS_PATH + f"{settings.model_name}-{IMAGE_SIZE}x{IMAGE_SIZE}-acc {rounded_acc:.3f}-id {id}.h5"
    graph_name = GRAPHS_PATH + f'graph-acc {rounded_acc:.3f}-'+id+'.png'

    # Write statistics to file
    f = open(STATS_FILE, 'a')
    f.write(";".join([
        model_name,
        graph_name,
        f"{rounded_acc:.3f}",
        f"{rounded_loss:.3f}",
        str(IMAGE_SIZE),
        str(settings)
    ]))
    f.close()

    # Returns generated names
    return (model_name, graph_name)

def save_graph(history: tf.keras.callbacks.History, 
                settings: ModelSettings, 
                graph_name: str) -> None:
    '''
    Generates graphs of accuracy and loss for a given training session,
    and saves them to GRAPHS folder.
    '''

    # Extract interesting statistics
    acc  = history.history['accuracy']
    loss = history.history['loss']
    val_acc  = history.history['val_accuracy']
    val_loss = history.history['val_loss']

    epochs_range = range(settings.epochs)

    
    plt.figure(figsize=(8, 8))
  
    # Creates 2 plots on one graph
    # First one represents the changing accuracy over epochs
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc='upper left')
    plt.title('Accuracy')

    # Second one represents the changing loss over epochs
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend(loc='upper left')
    plt.title('Loss')

    # Saves the figure to GRAPHS folder
    plt.savefig(graph_name)

def save_model(model:tf.keras.Sequential, model_name: str) -> None:
    '''
    Saves the model into the MODELS folder.
    '''

    model.save(model_name)
    print("[INFO] Saved model at {}".format(model_name))


def load_model(model_path:str):
    '''
    Loads the model from the path provided.
    '''
    model = tf.keras.models.load_model(model_path)
    model.summary()
    return model


def make_a_guess(model:tf.keras.Sequential, images:np.array):
    '''
    By using a given trained model, predicts the output(s) for the input image(s).\n
    Note that this has to be a 4D array, so 3D image must be reshaped into [1,image.shape].
    '''
    return model(images, training = False)


