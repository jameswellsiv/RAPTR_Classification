import cv2
import numpy as np
import image_utils
from matplotlib import pyplot as plt
from ColorIntensifier import intensifyColors

def classify_shape(img_filename, template_color):
    classification = 'none'
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    #---------------- Read the main image -----------------------------------------------------------
    img_rgb =  image_utils.read_image(img_filename, 1)

    #---------------- Read the triangle template ----------------------------------------------------
    triangle_template = cv2.imread('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Templates\\'+ template_color +'_triangle_template.jpg')
    triangle_template = cv2.resize(triangle_template, (150, 200))

    #---------------- Read the square template ------------------------------------------------------
    square_template = cv2.imread('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Templates\\'+ template_color +'_square_template.jpg')
    square_template = cv2.resize(square_template, (150, 200))

    #---------------- Read the circle template ------------------------------------------------------
    circle_template = cv2.imread('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Templates\\'+ template_color +'_circle_template.jpg')
    circle_template = cv2.resize(square_template, (150, 200))

    #---------------- Store width and heigth of the triangle template in w_tri and h_tri --------------------
    c, w_tri, h_tri = triangle_template.shape[::-1]
    print(w_tri, h_tri)

    #---------------- Store width and heigth of the square template in w_sq and h_sq ------------------------ 
    c_sq, w_sq, h_sq = square_template.shape[::-1]
    print(w_sq, h_sq)

    #---------------- Store width and heigth of the circle template in w_cir and h_cir ----------------------
    c_cir, w_cir, h_cir = circle_template.shape[::-1]
    print(w_cir, h_cir)

    #---------------- Show Templates and Main Image ---------------------------------------------------------
    #cv2.imshow('Triangle Template', triangle_template)
    #cv2.imshow('Square Template',square_template) 
    #cv2.imshow('Circle Template',circle_template) 
    #cv2.imshow('Image', img_rgb)
    #cv2.waitKey(0)
    
    #---------------- Template Matching Algorithm ----------------------------------------------------------- 

    # Specify a threshold 
    threshold = 0.95

    # Perform match operations. 
    res_triangle = cv2.matchTemplate(img_rgb,triangle_template, cv2.TM_CCORR_NORMED) 
    res_square = cv2.matchTemplate(img_rgb,square_template, cv2.TM_CCORR_NORMED)
    res_circle = cv2.matchTemplate(img_rgb,circle_template, cv2.TM_CCORR_NORMED)

    # Store the coordinates of matched area in a numpy array 
    loc_tri = np.where(res_triangle >= threshold) 
    loc_sq = np.where(res_square >= threshold) 
    loc_cir = np.where(res_circle >= threshold) 

    # Determine the area where there is a match with the template

    # Matched areas for triangle template
    tri_min_val, tri_max_val, tri_min_loc, tri_max_loc = cv2.minMaxLoc(res_triangle)
    top_left_tri = tri_max_loc
    bottom_right_tri = (top_left_tri[0] + w_tri, top_left_tri[1] + h_tri)

    # Matched areas for square template
    sq_min_val, sq_max_val, sq_min_loc, sq_max_loc = cv2.minMaxLoc(res_square)
    top_left_sq = sq_max_loc
    bottom_right_sq = (top_left_sq[0] + w_sq, top_left_sq[1] + h_sq)

    # Matched areas for circle template
    cir_min_val, cir_max_val, cir_min_loc, cir_max_loc = cv2.minMaxLoc(res_circle)
    top_left_cir = cir_max_loc
    bottom_right_cir = (top_left_cir[0] + w_cir, top_left_cir[1] + h_cir)

    print("Square Max Val: ", sq_max_val)
    print("Triangle Max Val: ", tri_max_val)
    print("Circle Max Val: ", cir_max_val)
    #---------------- Draw a rectangle around the matched region --------------------------------------------
    if (tri_max_val > sq_max_val and tri_max_val > cir_max_val):
        cv2.rectangle(img_rgb, top_left_tri, bottom_right_tri, 255, 2)
        classification = 'Triangle'
    elif (sq_max_val > tri_max_val and sq_max_val > cir_max_val):
        cv2.rectangle(img_rgb, top_left_sq, bottom_right_sq, 122, 2)
        classification = 'Square'
    elif (cir_max_val > tri_max_val and cir_max_val > sq_max_val):
        cv2.rectangle(img_rgb, top_left_cir, bottom_right_cir, 122, 2)
        classification = 'Circle'

    #---------------- Show the final image with the matched area -------------------------------------------- 
    #cv2.imshow('Detected',img_rgb) 
    #cv2.waitKey(0)
    return classification
