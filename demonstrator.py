import cv2
import numpy as np

from Src.loader import *
from Src.categorizer import *
from Src.const import *
from Src.settings import *
from Src.data_table import *

if __name__ == "__main__":
    verify_preprocessing_complete()
    
    mode = int(input("[INPUT] What would you like to do?\n1 - single image predictions, 2 - test images analysis: "))

    if mode != 1 and mode != 2:
        exit(1)

    model_name = input("[INPUT] Model path (leave empty for DEMO_MODEL): ")
    if(model_name == ""): model_name = DEMO_MODEL

    model = load_model(model_name)
    names = get_breeds()

    if mode == 1:
        while True:
            path = input("[INPUT] Image path (leave empty for DEMO_IMAGE, type 'exit' to exit): ")
            
            if path == "exit": exit(1)
            elif path == "": path = DEMO_FILE
            
            image = prepare_image_for_evaluation(path)
            output = make_a_guess(model, image)
            idx = np.argmax(output)
            predicted_breed = names[idx]
            score = output[0][idx]
            print(f"[PREDICTION] I think this is a {predicted_breed} ({score})")
            image_paths = get_example_images_for_breed(predicted_breed)

            plt.figure(figsize=(18, 6))

            plt.suptitle(f"It is a {predicted_breed}!", fontsize = 24)

            plt.subplot(1, 3, 1)
            img1 = cv2.imread(image_paths[0])
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            img1 = np.array(img1)
            plt.imshow(img1)

            img2 = cv2.imread(path)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            img2 = np.array(img2)
            plt.subplot(1, 3, 2)
            plt.imshow(img2)

            plt.subplot(1, 3, 3)
            img3 = cv2.imread(image_paths[1])
            img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
            img3 = np.array(img3)
            plt.imshow(img3)
            plt.savefig("output.png")
            print("[INFO] Output saved as output.png")


    else:
        images, labels,_ = load_images_labels(load_test_dataset=True)
        data_table = DataTable(names)
        
        output = make_a_guess(model, images)
        for i in range(output.shape[0]):
            correct = np.argmax(labels[i,:])
            guessed = np.argmax(output[i,:])
            if correct == guessed:
                data_table.at(correct).correct_guess()
            else:
                data_table.at(correct).incorrect_guess(names[guessed])
        
        data_table.save()
        print("[INFO] Statistics table has been created!")

    
        



