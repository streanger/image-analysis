#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from statistics import mean
import time

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        val = func(*args, **kwargs)
        after = time.time()
        print("elapsed time: {}s".format(round(after-before, 4)))
        return val
    return f    
    
def file_exists(file):
    if not os.path.exists(file):
        print("no such file:", file)
        sys.exit()

def save_file(file, image):
    imgDir = "analysed"
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    path = os.path.join(imgDir, file)
    cv2.imwrite(path, image)
    return True

def usage():
    print(">> put help content here...\n")
    return True

def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_image(img, newSize):
    height = round((img.shape[0])*(newSize/100))
    width = round((img.shape[1])*(newSize/100))
    resized = cv2.resize(img, (width, height))
    return resized    

@timer    
def main(args):
    # args = ['git_original.png', "100", "200"]
    if not args:
        usage()
        return False
    else:
        file = args[0]
        x_axis = int(args[1])
        y_axis = int(args[2])
    img = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    img = resize_image(img, 50)
    # b_channel, g_channel, r_channel, alpha_channel = cv2.split(img)
    # full_alpha = np.ones((img.shape[0], img.shape[1], 1), dtype='uint8')*255
    # new_img = cv2.merge((b_channel, g_channel, r_channel, full_alpha))
    
    img = roll_image(img, x_axis, y_axis)
    
    # show_image('rolled', img)
    cv2.imwrite("new_img.png", img)
    return True
    
def roll_image(img, x_axis, y_axis):
    img = np.roll(img, y_axis, axis=0)   # axis: 0-up-down, 1-right-left
    img = np.roll(img, x_axis, axis=1)   # axis: 0-up-down, 1-right-left
    return img
    
def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files


if __name__ == "__main__":
    path = script_path()
    main(sys.argv[1:])

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    