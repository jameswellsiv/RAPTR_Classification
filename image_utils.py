import cv2
import os
import time

def save_image(img, file_name):
    check = cv2.imwrite(file_name, img)
    return check

def read_image(file_name, num):
    image = cv2.imread(file_name, num)
    return image

def show_image(img_title, img):
    cv2.imshow(img_title,img) 
    cv2.waitKey(0)
    return

def resize_image(img, size_x=None, size_y=None):
    if size_x != None and size_y != None:
        img = cv2.resize(img, (size_x,size_y))
    else:
        img = cv2.resize(img, (300,300))
    return img

def crop_image(img_filename, plus_x, plus_y, crop_x=None, crop_y=None):
    img = read_image(img_filename, 1)
    if crop_x != None and crop_y != None:
        crop_img = img[crop_x:crop_x+plus_x, crop_y:crop_y+plus_y]
    else:
        crop_img = img[110:110+plus_x, 110:110+plus_y]
    return crop_img

def append_time_to_filename(img_filename):
    new_filename = ""
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = img_filename.split('.')
    new_filename = filename[0]+ '_' + timestr
    new_filename = new_filename + '.' + filename[1]
    return new_filename



def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)