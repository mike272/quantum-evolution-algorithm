from os import environ

####
#### This file contains constant values for the whole program
####

IMAGES_PATH  = './data/Images/'     # Folder containing multiple folders with dog images
ANNONS_PATH  = './data/Annotation/' # Folder containing annotations for the dog images
GRAPHS_PATH  = './Graphs/'          # Folder for where to store graphs
MODELS_PATH  = './Models/'          # Folder for where to store models after training

OUTPUTS_PATH = './Processed_Images/'        # Folder containing the augmented doggos images
PREPRC_PATH  = './Processed_Paths/'         # Folder containing files with paths and breeds of the dogs
STATS_FILE   = 'models_statistics.csv'      # File which stores statistics about every session
TEST_FILE    = 'test_set_statistics.csv'    # File which stores statistics of a test session run on a selected model


DEBUG = False               # Debug mode - loads/processes only a few images basically instant program execution
IMAGE_SIZE = 64             # Size to which all images and masks will be rescaled
DEMO_MODEL = 'alexGG.h5'    # Demo model used in demonstrations if no arguments were given
DEMO_FILE  = 'example.png'  # Demo image used in demonstrations if no arguments were given

if not DEBUG:
    # This silences obnoxious tensorflow messages
    environ['TF_CPP_MIN_LOG_LEVEL'] = "1"
else:
    environ['TF_CPP_MIN_LOG_LEVEL'] = "0"




