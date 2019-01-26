import sys
import os
import numpy as np
import cv2
import random


def script_path():
    '''set current path to script_path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def hexstring_to_color(data):
    ''' example -> #A0B0C0 '''
    if data.startswith('#'):
        data = data[1:]
    R, G, B = [int('0x' + data[n:n+2], 16) for n in range(0, len(data), 2)]
    return (R, G, B)
    
    
def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def random_color():
    return "{:06X}".format(random.randint(0, 0xFFFFFF))
    
    
def main(hexcolor):
    (R, G, B) = hexstring_to_color(hexcolor)
    pixel = np.array([[(R, G, B)]], dtype=np.uint8)
    resized = np.array(np.repeat(np.repeat(pixel, 500, axis=0), 500, axis=1))
    show_image(hexcolor, resized)                       # show
    # cv2.imwrite(hexcolor + '.png', resized)           # save
    return True
    
    
if __name__ == "__main__":
    script_path()
    # hexcolor = '#50F060'
    for x in range(10):
        hexcolor = random_color()
        main(hexcolor)

        
'''
todo:
    -change color dynamically
    -put color as hexstring or RGB  values
'''