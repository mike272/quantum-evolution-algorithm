from os import environ
from typing import Tuple

####
#### This file contains constant values for the whole program
####

STATS_FILE   = 'models_statistics.csv'      # File which stores statistics about every session
TEST_FILE    = 'test_set_statistics.csv'    # File which stores statistics of a test session run on a selected model

DEBUG = False               # Debug mode - loads/processes only a few images basically instant program execution

SCREEN_SIZE = [1280,720]
PIPE_IMAGE_SIZE = [200,3000]
FPS = 60

X_VELOCITY = 4
GRAVITY = 0.5
JUMP_POWER = 10
HOLE_SIZE = 250
HOLE_MIN_DIST = 50
COW_SCALE_DOWN = 2
COW_AMPLIFY_ROTATION = 6

ASSETS_PATH = "./Assets/"

if not DEBUG:
    # This silences obnoxious tensorflow messages
    environ['TF_CPP_MIN_LOG_LEVEL'] = "1"
else:
    environ['TF_CPP_MIN_LOG_LEVEL'] = "0"




