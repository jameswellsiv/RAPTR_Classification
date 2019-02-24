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
    timestamp = image_utils.get_timestamp() #Get timestamp for appending to the processed images for the image that was recieved at this time (recieved_image)
    print(timestamp)
    new_filename = image_utils.append_timestamp('RecievedImage.jpg', timestamp) #Append the timestamp to the image file that is about to be saved
    print(new_filename)
    save_check1 = image_utils.save_image(received_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Recieved_Images\\' + new_filename) #Save the received image with its timestamp appended
   
    if save_check1 is True:
        print('Saved ' + new_filename)

    #---------------- Resize the recieved image ---------------------------------------------------------
    resized_image = image_utils.resize_image(received_image) #Resize image to 300 px by 300 px
    new_filename2 = image_utils.append_timestamp('ResizedImage.jpg', timestamp) #Append timestamp to resized image file
    save_check2 = image_utils.save_image(resized_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\' + new_filename2) #Save the resized image with its timestamp appened, note this is the same timestamp as new_filename
   
    if save_check2 is True:
        print('Saved ' + new_filename2)
        #image_utils.del_image(img_filename) #Deleting image in Trigger Folder so next image can Trigger the watchdog

    #intensified_image = intensifyColors('resized_image1.jpg') #Intensify colors in image
    #save_check2 = image_utils.save_image(intensified_image, 'intensified_image1.jpg')

    #---------------- Crop out the center of the resized image -----------------------------------------------------------
    cropped_image = image_utils.crop_image('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\' + new_filename2, 90, 90) #Crop out a 80 px by 80 px box the center of the resized image for dominant color determination
    new_filename3 = image_utils.append_timestamp('CroppedImage.jpg', timestamp)
    save_check3 = image_utils.save_image(cropped_image, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Cropped_Images\\' + new_filename3) #Save the cropped image with its timestamp appended, note this is the same timestamp as new_filename and new_filename2
    
    if save_check3 is True:
        print('Saved ' + new_filename3)

    #---------------- Determine the most dominant color in the center of the image ---------------------------------------
    dominant_RGB = most_frequent_colour('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Cropped_Images\\' + new_filename3) #Pass through the crop image of the most recently recieved image for determining the dominant color in that image
    #print(dominant_RGB)

    #---------------- Choose Template color based off the most dominant color in the center of the image (RGB Values Comparison) -----------------
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
        object_classification = classify_shape('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\' + new_filename2, template_color) #Found the most dominant color in image, now pass through the resized image of the image used in the Dominant Color Determination, NOT the cropped image
        print(object_classification)
        #image_utils.toc()
        print()
        return object_classification, 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Resized_Images\\' + new_filename2 #Return the classification and the resized image for displaying on the GUI
    else:
        print("Couldn't detect color")
        return 'none', 'none'