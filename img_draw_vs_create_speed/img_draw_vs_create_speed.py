import sys
import os
import time
import random
import math
import numpy as np
import cv2


def blank_image(height, width, layers=3, value=255):
    '''create blank image, with specified shape, layers and initial value'''
    img = np.ones((height, width, layers), dtype=np.uint8)*value
    return img
    
    
def img_paint_vs_create(height, width, iterations, create=True):
    '''creating new image vs painting the same'''
    img = blank_image(height, width, layers=3, value=0)
    if create:
        for x in range(iterations):
            img = blank_image(height, width, layers=3, value=0)
    else:
        for x in range(iterations):
            img[:, :] = 0
    return None
    
    
if __name__ == "__main__":
    height, width = 1080, 1920
    iterations = 1000
    
    # create new image for x iterations
    begin = time.time()
    create = True
    img_paint_vs_create(height, width, iterations, create)
    print('create: {}, elapsed: {}[s]'.format(create, time.time() - begin))
    # create: True, elapsed: 16.603949785232544[s]
    
    # create image one time and then paint it black
    begin = time.time()
    create = False
    img_paint_vs_create(height, width, iterations, create)
    print('create: {}, elapsed: {}[s]'.format(create, time.time() - begin))
    # create: False, elapsed: 0.4090235233306885[s]
    
    
    # CONCLUSION: painting is much faster than creating new image
