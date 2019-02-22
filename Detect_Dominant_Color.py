import struct
from PIL import Image
from save_image import save_image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

NUM_CLUSTERS = 5

def most_frequent_colour(img_filename):

    img = Image.open(img_filename)
    w, h= img.size
    pixels = img.getcolors(w * h)

    most_frequent_pixel = pixels[0]
    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    print("Most Common", img, most_frequent_pixel[1])
    

    return most_frequent_pixel[1]