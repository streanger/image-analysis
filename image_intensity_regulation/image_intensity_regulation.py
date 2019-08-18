'''
script for regulation image intesity
version: 1.0.1
added:
    make_contrast_images
'''

import sys
import os

import cv2
import numpy as np


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
            
            
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
    
    
def make_contrast_images(files, dir):
    '''increase all image pixels to diff between 255 and max pixel value; dir - out directory'''
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    for file in files:
        filename = os.path.basename(os.path.normpath(file))
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        max_value = img.max()
        img += 255 - max_value + 1
        out = os.path.join(dir, filename)
        print(out)
        cv2.imwrite(out, img)
    return True
    
    
def detailed_analysis(files):
    '''detailed analysis of every single image, with interactive mode'''
    cv2.namedWindow('out', cv2.WINDOW_FULLSCREEN)
    for file in files[:]:
        print(file)
        print('skip or save or enter to continue')
        img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        for x in range(256):
            out = image_intensity_regulation(img, x)
            # show_image('out', out)
            cv2.imshow('out', out)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            print('\t', x)
            if not x%5:
                ask = input()
                if ask == 'skip':
                    break
                elif ask == 'save':
                    cv2.imwrite('out_{}.png'.format(x), out)
        cv2.destroyAllWindows()
    return True
    
    
if __name__ == "__main__":
    script_path()
    dir = 'zadanie_nr_1'
    files = list(filter(lambda x: x.endswith('.png'), absoluteFilePaths(dir)))
    
    
    # ****************** detailed analysis ******************
    # detailed_analysis(files)
    
    
    # ****************** full contrast ******************
    make_contrast_images(files, dir + '_contrasted')
    
'''
todo:
    -think of combing layers - something may be hidden into both 0 and 1st bit_length
    -
    
'''
