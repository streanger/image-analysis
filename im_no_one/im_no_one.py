#!/usr/bin/python3
import sys
import os
import time
import random
import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
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
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def blank_image(height, width, layers=3):
    img = np.ones((height, width, layers), dtype=np.uint8)*0
    return img
    
    
def generate_points(diff=30, height=30, start_x=100, start_y=50):
    # diff = 30
    # height = 30
    color = (50, 50, 255)
    # start_x = 100
    # start_y = 50
    thickness = 2
    img = blank_image(150, 400)
    
    points_pairs = []
    
    # verticals
    for key in range(15):
        if key == 1:
            img = cv2.line(img, (start_x + diff*key, start_y), (start_x + diff*key, start_y + 20), color, thickness)    # '
            points_pairs.append(((start_x + diff*key, start_y), (start_x + diff*key, start_y + 20)))
        elif key == 14:
            img = cv2.line(img, (start_x + diff*key, start_y + 10), (start_x + diff*key, start_y + 20), color, thickness)    # e
            points_pairs.append(((start_x + diff*key, start_y + 10), (start_x + diff*key, start_y + 20)))
        else:
            img = cv2.line(img, (start_x + diff*key, start_y + 10), (start_x + diff*key, start_y + 10 + height), color, thickness)   # else
            points_pairs.append(((start_x + diff*key, start_y + 10), (start_x + diff*key, start_y + 10 + height)))
            
            
    # horizontals
    img = cv2.line(img, (start_x + diff*2, start_y + 10), (start_x + diff*4, start_y + 10), color, thickness)                     # m
    points_pairs.append(((start_x + diff*2, start_y + 10), (start_x + diff*4, start_y + 10)))
    img = cv2.line(img, (start_x + diff*5, start_y + 10), (start_x + diff*6, start_y + 10), color, thickness)                     # n
    points_pairs.append(((start_x + diff*5, start_y + 10), (start_x + diff*6, start_y + 10)))
    img = cv2.line(img, (start_x + diff*7, start_y + 10), (start_x + diff*8, start_y + 10), color, thickness)                     # o
    points_pairs.append(((start_x + diff*7, start_y + 10), (start_x + diff*8, start_y + 10)))
    img = cv2.line(img, (start_x + diff*7, start_y + 10 + height), (start_x + diff*8, start_y + 10 + height), color, thickness)   # o
    points_pairs.append(((start_x + diff*7, start_y + 10 + height), (start_x + diff*8, start_y + 10 + height)))
    
    img = cv2.line(img, (start_x + diff*9, start_y + 10), (start_x + diff*10, start_y + 10), color, thickness)                     # o
    points_pairs.append(((start_x + diff*9, start_y + 10), (start_x + diff*10, start_y + 10)))
    img = cv2.line(img, (start_x + diff*9, start_y + 10 + height), (start_x + diff*10, start_y + 10 + height), color, thickness)   # o
    points_pairs.append(((start_x + diff*9, start_y + 10 + height), (start_x + diff*10, start_y + 10 + height)))
    img = cv2.line(img, (start_x + diff*11, start_y + 10), (start_x + diff*12, start_y + 10), color, thickness)                     # n
    points_pairs.append(((start_x + diff*11, start_y + 10), (start_x + diff*12, start_y + 10)))
    img = cv2.line(img, (start_x + diff*13, start_y + 10), (start_x + diff*14, start_y + 10), color, thickness)                     # e
    points_pairs.append(((start_x + diff*13, start_y + 10), (start_x + diff*14, start_y + 10)))
    img = cv2.line(img, (start_x + diff*13, start_y + 20), (start_x + diff*14, start_y + 20), color, thickness)                     # e
    points_pairs.append(((start_x + diff*13, start_y + 20), (start_x + diff*14, start_y + 20)))
    img = cv2.line(img, (start_x + diff*13, start_y + 10 + height), (start_x + diff*14, start_y + 10 + height), color, thickness)   # e
    points_pairs.append(((start_x + diff*13, start_y + 10 + height), (start_x + diff*14, start_y + 10 + height)))
    
    
    # show_image('img', img)
    # cv2.imwrite('img.png', img)
    return points_pairs
    
    
def make_video(images, outvid="video.avi", fps=5, size=None,
               is_color=True, format="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    imNumber = len(images)
    for key, file in enumerate(images):
        print(file)
        img = cv2.imread(file)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
        #print("Progress: {0}%".format((key+1)/imNumber*100), end="\r", flush=True)
    cv2.destroyAllWindows()
    vid.release()
    return vid
    
    
def make_video(points_pairs, outvid="video.avi", fps=5, size=None, is_color=True, format="XVID"):
    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None

    color = (50, 50, 255)
    thickness = 3
    img = blank_image(150, 600)
    points_pairs.insert(0, ((0, 0), (0, 0)))
    points_pairs += [points_pairs[-1]]*10
    for key, (p1, p2) in enumerate(points_pairs):
        if key:
            img = cv2.line(img, p1, p2, color, thickness)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
    vid.release()
    return vid
    
    
if __name__ == "__main__":
    path = script_path()
    points_pairs = generate_points(diff=30, height=30, start_x=100, start_y=50)
    make_video(points_pairs, outvid="video.avi", fps=3, size=None, is_color=True, format="XVID")
    # sys.exit()
    
    color = (50, 50, 255)
    thickness = 3
    new = blank_image(150, 600)
    for (p1, p2) in points_pairs:
        new = cv2.line(new, p1, p2, color, thickness)
        
        time.sleep(0.2)
        cv2.imshow('new', new)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    
    show_image('new', new)
    cv2.imwrite('new.png', new)
    
    
'''
the most useless script i have ever done
'''
