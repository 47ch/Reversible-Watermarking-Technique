from PIL import Image
import numpy as np
import math
import random

def cubic_based_bicubic_interpolation_algorithm(image_path):
    """
    Prediction algorithm for set B.
    Set is divided into 2 subcategories: adjacent to boundary and non-adjacent
    Adjacent to boundary uses a simple calculation that calculates average of reference pixels.
    Non-adjacent uses a combination of W_func and reference pixels to predict pixel value.
    """

    # Load the decrypted image
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size
    set_b = []

    for m in range((height/2) - 1):
        for n in range((width/2)-1):
            set_b.append((2*m,2*n))

    for pixel in set_b:
        if pixel[0] == 1:
            resulting_pixel = (pixel_map[pixel[0]-1,pixel[1]-1] +
                               pixel_map[pixel[0]-1,pixel[1]+1] + 
                               pixel_map[pixel[0]+1,pixel[1]-1] + 
                               pixel_map[pixel[0]+1,pixel[1]+1] + 
                               2*pixel_map[pixel[0]-1,pixel[1]])/6
            
        elif pixel[0] == width - 2:
            resulting_pixel = (pixel_map[pixel[0]+1,pixel[1]-1] +
                               pixel_map[pixel[0]+1,pixel[1]+1] + 
                               pixel_map[pixel[0]-1,pixel[1]-1] + 
                               pixel_map[pixel[0]-1,pixel[1]+1] + 
                               2*pixel_map[pixel[0]+1,pixel[1]])/6
            
        elif pixel[1] == 1:
            resulting_pixel = (pixel_map[pixel[0]+1,pixel[1]-1] +
                               pixel_map[pixel[0]+1,pixel[1]+1] + 
                               pixel_map[pixel[0]-1,pixel[1]-1] + 
                               pixel_map[pixel[0]-1,pixel[1]+1] + 
                               2*pixel_map[pixel[0],pixel[1]-1])/6
            
        elif pixel[1] == height - 2:
            resulting_pixel = (pixel_map[pixel[0]+1,pixel[1]-1] +
                               pixel_map[pixel[0]+1,pixel[1]+1] + 
                               pixel_map[pixel[0]-1,pixel[1]-1] + 
                               pixel_map[pixel[0]-1,pixel[1]+1] + 
                               2*pixel_map[pixel[0],pixel[1]+1])/6
            
        else:
            resulting_pixel = ( W_func(0.5)*W_func(0.5)*((pixel_map[pixel[0]-1,pixel[1]]) +
                                                       (pixel_map[pixel[0],pixel[1]-1]) +
                                                       (pixel_map[pixel[0]+1,pixel[1]]) + 
                                                       (pixel_map[pixel[0],pixel[1]+1])) +

                                W_func(0.5)*W_func(1.5)*((pixel_map[pixel[0]-2,pixel[1]-1]) +
                                                         (pixel_map[pixel[0]-2,pixel[1]-1]) +
                                                         (pixel_map[pixel[0]+1,pixel[1]-2]) +
                                                         (pixel_map[pixel[0]+2,pixel[1]-1]) +
                                                         (pixel_map[pixel[0]+2,pixel[1]+1]) +
                                                         (pixel_map[pixel[0]+1,pixel[1]+2]) +
                                                         (pixel_map[pixel[0]-1,pixel[1]+2]) +
                                                         (pixel_map[pixel[0]-2,pixel[1]+1])) +

                                W_func(1.5)*W_func(1.5)*((pixel_map[pixel[0]-1,pixel[1]-1]) +
                                                         (pixel_map[pixel[0]+1,pixel[1]-1]) +
                                                         (pixel_map[pixel[0]+1,pixel[1]+1]) +
                                                         (pixel_map[pixel[0]-1,pixel[1]+1])))
            
        pixel_map[pixel[0],pixel[1]] = resulting_pixel
            

    

def W_func(x):
    x = abs(x)
    if x <=1:
        return_value = 1.5*(x**3) - 2.5*(x**2) + 1
    elif 1 < x and x < 2:
        return_value = -0.5*(x**3) + 2.5*(x**2) - 4*x + 2   
    else:
        return_value = 0
    
    return return_value

