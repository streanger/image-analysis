'''
this is very copied script
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_grabcut/py_grabcut.html
'''

import os
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt



def script_path():
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current)
    return current
    
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    script_path()
    # file = 'messi.jpg'
    file = 'very_test.png'
    # file = 'test.png'
    # files = [item for item in os.listdir() if item.endswith(('.png', '.jpg'))]
    
    
    img = cv2.imread(file)
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    
    height, width = img.shape[:2]
    # rect = (50, 50, 450, 290)
    rect = (50, 50, 480, 310)
    # rect = (0, 0, height, width)
    print(rect)
    
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:, :, np.newaxis]
    show_image('img', img)
    # plt.imshow(img),plt.colorbar(),plt.show()
    
    
    if False:
        # newmask is the mask image I manually labelled
        newmask = cv2.imread('newmask.png', 0)

        # whereever it is marked white (sure foreground), change mask=1
        # whereever it is marked black (sure background), change mask=0
        mask[newmask == 0] = 0
        mask[newmask == 255] = 1

        mask, bgdModel, fgdModel = cv2.grabCut(img ,mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

        mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask[:, :, np.newaxis]
        plt.imshow(img)
        plt.colorbar()
        plt.show()
        
        