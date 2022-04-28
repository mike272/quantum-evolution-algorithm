import cv2
import os

from xml.etree.ElementTree import parse as parse_annotation
from shutil import rmtree as delete_contents

from Src.const import *

OFFSETS = [(0,0)] #[(-5,0),(0,5),(0,0),(0,-5),(5,0)]:

def perform_data_augmentation():

    ssize = input("[INFO] Target image size (single integer, empty for default 64): ")
    if(ssize == ""): ssize = "64"
    size = int(ssize)

    if not os.path.exists(OUTPUTS_PATH):
        os.mkdir(OUTPUTS_PATH)
    if not os.path.exists(PREPRC_PATH):
        os.mkdir(PREPRC_PATH)

    if not os.path.exists(OUTPUTS_PATH+ssize) and not os.path.exists(OUTPUTS_PATH+ssize+"-test"):
        os.mkdir(OUTPUTS_PATH+ssize)
        os.mkdir(OUTPUTS_PATH+ssize+"-test")
    else:
        decision = input("[INFO] This process will delete the previous augmentation results for this image size. Continue? Y/N: ")
        if(not decision.lower() == "y"): exit(1)

        print("[INFO] Deleting previous preprocessing results...")
        if(os.path.exists(OUTPUTS_PATH+ssize)):
            delete_contents(OUTPUTS_PATH+ssize)
        if(os.path.exists(OUTPUTS_PATH+ssize+"-test")):
            delete_contents(OUTPUTS_PATH+ssize+"-test")

        os.mkdir(OUTPUTS_PATH+ssize)
        os.mkdir(OUTPUTS_PATH+ssize+"-test")

    doggos_directory = os.listdir(IMAGES_PATH)

    doggos_files  = ['']*len(doggos_directory)
    doggos_folders = ['']*len(doggos_directory)

    paths_file = open(PREPRC_PATH+ssize+".csv", 'w')
    paths_tests_file = open(PREPRC_PATH+ssize+"-test.csv", 'w')
    paths_file.write("doggo_path;doggo_breed\n")
    paths_tests_file.write("doggo_path;doggo_breed\n")

    count = 0
    for iterator, dog_folder in enumerate(doggos_directory):
        dog_images = os.listdir(IMAGES_PATH+dog_folder)
        count += len(dog_images)

        doggos_files[iterator] = dog_images
        doggos_folders[iterator] = dog_folder
    
    i = 0
    for folder, files in zip(doggos_folders, doggos_files):
        for doggo_file in files:
            if(i%10<2):
                save_as_test_image(folder, doggo_file, paths_tests_file, size, str(i))
            else:
                augment_image(folder, doggo_file, paths_file, size, str(i))
            print_animated_loader(i, count)
            i += 1
            if DEBUG: break
        if DEBUG: break
        
    paths_file.close()
    print("\n[HOORAY] Process completed successfully!")

def save_as_test_image(folder, doggo_file, paths_file, size, id):

    doggo_path_without_extension = folder+'/'+ doggo_file.split('.')[0]
    doggo_breed = extract_breed_from_folder_name(folder)

    tree = parse_annotation(ANNONS_PATH + doggo_path_without_extension)
    root = tree.getroot()

    for match in root.iter('xmax'):
        xmax = int(match.text)
    for match in root.iter('xmin'):
        xmin = int(match.text)
    for match in root.iter('ymax'):
        ymax = int(match.text)
    for match in root.iter('ymin'):
        ymin = int(match.text)
    
    image = cv2.imread(IMAGES_PATH + doggo_path_without_extension + '.jpg')
    image = image[ymin : ymax,  xmin : xmax]
    image = cv2.resize(image, (size, size), interpolation = cv2.INTER_CUBIC)

    save_test_image_and_path(image, size, id, doggo_breed, paths_file)


def augment_image(folder, doggo_file, paths_file, size, id):

    doggo_path_without_extension = folder+'/'+ doggo_file.split('.')[0]
    doggo_breed = extract_breed_from_folder_name(folder)

    tree = parse_annotation(ANNONS_PATH + doggo_path_without_extension)
    root = tree.getroot()

    for match in root.iter('xmax'):
        xmax = int(match.text)
    for match in root.iter('xmin'):
        xmin = int(match.text)
    for match in root.iter('ymax'):
        ymax = int(match.text)
    for match in root.iter('ymin'):
        ymin = int(match.text)
    
    image = cv2.imread(IMAGES_PATH + doggo_path_without_extension + '.jpg')
    
    ythresh,xthresh,_ = image.shape
    
    for xoffset, yoffset in OFFSETS:
        try:
            x = str(xoffset)
            y = str(yoffset)

            img = image[
                max(ymin+yoffset,0) : min(ymax+yoffset,ythresh), 
                max(xmin+xoffset,0) : min(xmax+xoffset,xthresh)
            ]
 
            img = cv2.resize(img, (size, size), interpolation = cv2.INTER_CUBIC)
            save_image_and_path(img, size, x, y, id, '', doggo_breed, paths_file)

            flipped = cv2.flip(img,1)
            save_image_and_path(flipped, size, x, y, id, 'f', doggo_breed, paths_file)

            #blurred = cv2.blur(img, (2,2))
            #save_image_and_path(blurred, size, x, y, id, 'b', doggo_breed, paths_file)

            #flip_blur = cv2.blur(flipped,(2,2))
            #save_image_and_path(flip_blur, size, x, y, id, 'fb', doggo_breed, paths_file)

        except Exception as e: 
            print(e)
            print("[WARN] Error in processing {}".format(doggo_path_without_extension))


def extract_breed_from_folder_name(file:str):
    breed = file.split('-')[1:]
    breed = ' '.join(breed)
    breed = breed.replace('_',' ')
    breed = breed.lower()
    return breed

def save_test_image_and_path(image, size, id, doggo_breed, paths_file):
    path = OUTPUTS_PATH + str(size) + '-test/' + id  + '.png'
    cv2.imwrite(path, image)
    paths_file.write("{};{}\n".format(path,doggo_breed))

def save_image_and_path(image, size, x, y, id, t, doggo_breed, paths_file):
    path = OUTPUTS_PATH + str(size) + '/' + id + x + y + t + '.png'
    cv2.imwrite(path, image)
    paths_file.write("{};{}\n".format(path,doggo_breed))

def print_animated_loader(i, count):
    if (i%8<=1):  c = '\\'
    elif(i%8<=3): c = '|'
    elif(i%8<=5): c = '/'
    else:         c = '-'
    
    print("\r[LOAD] {} Processing and augmenting images... {}/{} {}".format(c,i+1,count,c),end="")

if __name__ == "__main__":
    perform_data_augmentation()