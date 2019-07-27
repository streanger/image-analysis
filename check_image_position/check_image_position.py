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
    
    
def create_blank_image(height, width):
    image = np.zeros((height, width, 3), np.uint8)
    image += 55
    return image
    
    
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
    
    
def check_position(file1, pos1, file2, pos2):
    # ************** check position **************
    heightMain, widthMain = 900, 1200
    blank = create_blank_image(heightMain, widthMain)
    # blank = create_image(heightMain, widthMain)               # with some predefined background
    # img = draw_tv_background_and_backlight(blank)       # draw some background(for now return the same image)
    img = blank.copy()
    
    # read first image
    # file = 'th_view_02.png'
    stable = cv2.imread(file1, cv2.IMREAD_UNCHANGED)
    # img = paste_image(stable, img, 400, 388)
    img = paste_image(stable, img, pos1[0], pos1[1])
    
    # read second image
    # second = 'th_view_03.png'
    loaded = cv2.imread(file2, cv2.IMREAD_UNCHANGED)
    # pos_x, pos_y = 200, 200
    pos_x, pos_y = pos2
    size_y, size_x = loaded.shape[:2]
    
    firstTick = True
    while True:
        if firstTick:
            out = img*1
            firstTick = False
        else:
            try:
                if pos_x < 0:
                    pos_x = 0
                if pos_x > widthMain:
                    pos_x = widthMain
                    
                if pos_y < 0:
                    pos_y = 0
                if pos_y > heightMain:
                    pos_y = heightMain
                
                print("pos_x: {:4d}, pos_y: {:4d}".format(pos_x, pos_y), end='\r', flush=True)
                out = paste_image(loaded, img, pos_x, pos_y)
            except:
                continue
                
                
        cv2.imshow('out', out)
        
        # this could be handled some dictio way?
        key = cv2.waitKey(33)
        if key == -1:
            pass
            
        elif key == 119:
            # W - 119
            pos_y -= 1
            
        elif key == 115:
            # S - 115
            pos_y += 1
            
        elif key == 97:
            # A - 97
            pos_x -= 1
            
        elif key == 100:
            # D - 100
            pos_x += 1
            
        elif key == 116:
            # T - 116
            pos_y -= 10
            
        elif key == 103:
            # G - 103
            pos_y += 10
            
        elif key == 102:
            # F - 102
            pos_x -= 10
            
        elif key == 104:
            # H - 104
            pos_x += 10
            
        elif key == ord('q'):
            break
            
        else:
            # print(key)
            pass
            
    cv2.destroyAllWindows()
    print()
    return True
    
    
if __name__ == "__main__":
    currentPath = script_path()
    
    file1 = 'th_view_02.png'
    file2 = 'th_view_03.png'
    check_position(file1, (300, 300), file2, (200, 200))
