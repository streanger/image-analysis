import sys
import os

import cv2
import numpy as np


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def image_intensity_regulation(img, value):
    ''' value can be in range from -255 to 255 '''
    out = img + value
    return out
    
    
if __name__ == "__main__":
    script_path()
    file = "hidden.png"
    
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    for x in range(256):
        out = image_intensity_regulation(img, x)
        show_image('out', out)
        print(x)
        
    '''
    some = img.tolist()
    for key, line in enumerate(some):
        if not key%10:
            print(key, line)
            input()
    '''
