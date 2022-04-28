# NOTE - Fresh project - expect further changes in the future
# YOLO Cancer Detection


## Project description


* [X] Prepare basic project structure
* [] Implement YOLO weights loading - CURRENTLY IN PROGRESS

## Before Running

1. Download the following dataset: (Included in raport)
2. Extract the folders: *Images* from *images* directory and *Annotation* from *annotations*
3. Place extracted folders to *data* folder
4. In the command line, navigate to the folder directory and run (preferably on a fresh python environment):
   Windows:
   `python -m pip install -r requirements.txt`
   Linux/Mac:
   `python3 -m pip install -r requirements.txt`

## Data Preprocessing and Augmentation, Data Split

In order to reduce the chance of overfitting and improve the accuracy on the test set, the solution comes with a preprocessing script. The code is designed to reduce the images' size to reduce memory usage, augment the data using the flip, blur, x- and y- offsets, and generate a test set (20% of the data)

**Data split for this project: 70% training, 10% validation, 20% testing**

To perform preprocessing (**MANDATORY TO LAUNCH DEMO**)

1. Run preprocessor.py
   `python preprocessor.py`
2. When prompted for image size, leave empty for default (64). Alternatively, you can use any other - remeber to change IMAGE_SIZE constant in *Src/const.py*

## Tested Models


## Solution Description


## Results

