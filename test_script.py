from Detect_Dominant_Color import most_frequent_colour
from ColorIntensifier import intensifyColors
from TemplateMatching import classify_shape
import image_utils
from PIL import Image
import numpy as np
import cv2
import scipy.misc

def test_script(img_filename):
    
    #image_utils.tic()
    #---------------- Read the recieved image -----------------------------------------------------------
    received_image = image_utils.read_image(img_filename, 1) #Read in image to numpy array
    new_filename = image_utils.append_time_to_filename(img_filename)
    print(new_filename)
    save_check1 = image_utils.save_image(received_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Recieved_Images\\received_image1.jpg') #Save the received image
    print(save_check1)
    if save_check1 is True:
        print('Saved received_image1.jpg')

    #---------------- Resize the recieved image ---------------------------------------------------------
    resized_image = image_utils.resize_image(received_image) #Resize image to 300 px by 300 px
    save_check2 = image_utils.save_image(resized_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\resized_image1.jpg') #Save the resized image
    if save_check2 is True:
        print('Saved resized_image1.jpg')

    #intensified_image = intensifyColors('resized_image1.jpg') #Intensify colors in image
    #save_check2 = image_utils.save_image(intensified_image, 'intensified_image1.jpg')

    #---------------- Crop out the center of the resized image -----------------------------------------------------------
    cropped_image = image_utils.crop_image('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\resized_image1.jpg', 90, 90) #Crop out a 80 px by 80 px box the center of the image for dominant color determination
    #image_utils.show_image(cropped_image, 'Cropped Image') #Show the image
    save_check3 = image_utils.save_image(cropped_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Cropped_Images\\cropped_image1.jpg') #Save the cropped image
    if save_check3 is True:
        print('Saved cropped_image1.jpg')

    #---------------- Determine the most dominant color in the center of the image ---------------------------------------
    dominant_RGB = most_frequent_colour('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Cropped_Images\\cropped_image1.jpg')
    print(dominant_RGB)

    #---------------- Choose Template color based off the most dominant color in the center of the image -----------------
    if(dominant_RGB[2] > 0 and dominant_RGB[2] < 102):
        if(dominant_RGB[1] > 102 and dominant_RGB[2] < 255):
            print("Dominant color is yellow")
            template_color = "yellow"
        elif(dominant_RGB[1] > 0 and dominant_RGB[2] < 102):
            print("Dominant color is red")
            template_color = "red"
    elif(dominant_RGB[2] > 102 and dominant_RGB[2] < 255):
        print("Dominant color is blue")
        template_color = "blue"
    else:
        print("No color found")
        template_color = "none"

    #---------------- Classify the shape in the image --------------------------------------------------------------------
    if(template_color != "none"):
        object_classification = classify_shape('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\resized_image1.jpg', template_color)
        print(object_classification)
        #image_utils.toc()
        print()
        return object_classification, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\resized_image1.jpg'
    else:
        print("Couldn't detect color")
        return 'none', 0