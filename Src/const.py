from os import environ

####
#### This file contains constant values for the whole program
####

STATS_FILE   = 'models_statistics.csv'      # File which stores statistics about every session

DEBUG = False               # Debug mode - loads/processes only a few images basically instant program execution

SCREEN_SIZE = [1280,720]
PIPE_IMAGE_SIZE = [200,1000]
FPS = 60

INPUT_SHAPE = 2
X_VELOCITY = 4
GRAVITY = 0.5

PIPE_DIST = 600
HOLE_SIZE = 250
HOLE_MIN_DIST = 50

COW_JUMP_POWER = 10
COW_X = 100
ORIGINAL_COW_SIZE = [320,320]
COW_SCALE_DOWN = 2
COW_SIZE = [ORIGINAL_COW_SIZE[0]//COW_SCALE_DOWN,ORIGINAL_COW_SIZE[1]//COW_SCALE_DOWN]
COW_AMPLIFY_ROTATION = 6
COW_TOUCH_OFFSET = 50

ASSETS_PATH = "./Assets/"

if not DEBUG:
    # This silences obnoxious tensorflow messages
    environ['TF_CPP_MIN_LOG_LEVEL'] = "1"
else:
    environ['TF_CPP_MIN_LOG_LEVEL'] = "0"




