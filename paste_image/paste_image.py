''' paste one image into another, with handling size '''
import sys
import os
import time
import random
import numpy as np
import cv2


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def create_image(height, width):
    img = np.array(range(height*width), dtype=np.uint8).reshape((width, height))        # create one layer array
    out = np.stack((img,)*3, axis=-1)                                                   # convert 1 layer to 3 layer (gray -> rgb)
    return out
    
    
def paste_image(smaller, bigger, x_pos, y_pos):
    ''' paste some image with alpha channel, to another one '''
    
    # ************** handle position and size errors **************
    max_size_y , max_size_x = bigger.shape[:2]
    small_size_y, small_size_x = smaller.shape[:2]
    cut_x, cut_y = 0, 0
    if x_pos + small_size_x > max_size_x:
        cut_x = max_size_x - x_pos
        if cut_x < 1:
            return bigger
        smaller = smaller[:, 0:cut_x]
    if y_pos + small_size_y > max_size_y:
        cut_y = max_size_y - y_pos
        if cut_y < 1:
            return bigger
        smaller = smaller[0:cut_y, :]
    # print("cut_x: {:0=3d}, cut_y: {:0=3d}".format(cut_x, cut_y), end='\r', flush=True)
    
    
    # ************** paste smaller image into bigger, with including alpha channel **************
    B, G, R, alpha = cv2.split(smaller)
    smallerRGB = cv2.merge((B, G, R))
    mask_inv = cv2.bitwise_not(alpha)
    height, width = smallerRGB.shape[:2]
    
    roi = bigger[y_pos:y_pos+height, x_pos:x_pos+width]
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(smallerRGB, smallerRGB, mask=alpha)
    
    dst = cv2.add(img1_bg, img2_fg)
    out = bigger.copy()         # we shouldn't change original image
    out[y_pos:y_pos+height, x_pos:x_pos+width] = dst
    return out
    
    
if __name__ == "__main__":
    currentPath = script_path()
    
    smaller = cv2.imread('pigeon.png', cv2.IMREAD_UNCHANGED)
    heightMain, widthMain = 1200, 900
    bigger = create_image(heightMain, widthMain)
    
    if False:
        out = paste_image(smaller, bigger, 580, 600)
        show_image('out', out)
    else:
        for x in range(50):
            out = paste_image(smaller, bigger, 20*x+200, 20*x)
            cv2.imshow('out', out)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.04)     # is it really needed?
            # input()
        cv2.destroyAllWindows()
