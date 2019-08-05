import sys
import os
import time
import random
import numpy as np
import cv2
import winsound
import pkg_resources    # this is for read static package files


def script_path():
    ''' return and change directory, to current script path '''
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
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
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    # cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def paste_image_up_down(smaller, bigger, x_pos, y_pos, line_size=2, line_time=0.001):
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
    # out[y_pos:y_pos+height, x_pos:x_pos+width] = dst
    
    
    # check shape again, with correct image
    small_size_y, small_size_x = smaller.shape[:2]
    for y in range(small_size_y):
        # out[y_pos:y_pos+height, x_pos:x_pos+width] = dst[y, :]
        out[y_pos+y:y_pos+y+1+line_size, x_pos:x_pos+width] = dst[y, :]
        cv2.imshow('img', out)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(line_time)
    input('press enter, to exit... ')
    cv2.destroyAllWindows()
    return out
    
    
if __name__ == "__main__":
    script_path()
    small = 'hedgehog.png'
    big = 'green_grass.jpg'
    smaller = cv2.imread(small, cv2.IMREAD_UNCHANGED)
    bigger = cv2.imread(big, 1)
    
    out = paste_image_up_down(smaller, bigger, 250, 125, line_size=5, line_time=0.002)
    