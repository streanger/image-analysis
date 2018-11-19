#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from statistics import mean

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

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
    print("put help content here...\n")
    sys.exit()

def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def roll_image(img, x_axis, y_axis):
    img = np.roll(img, y_axis, axis=0)   # axis: 0-up-down, 1-right-left
    img = np.roll(img, x_axis, axis=1)   # axis: 0-up-down, 1-right-left
    return img
    
def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

def rgb_roll(file):
    ''' todo: set parameters to roll: rotation & radius (R-G-B are set between 120 deg) '''
    image = cv2.imread(file)
    show_image("before", image)
    b_channel, g_channel, r_channel = cv2.split(image)      # split to R-G-B
    b_channel = roll_image(b_channel, 0, -14)                # move each one
    g_channel = roll_image(g_channel, 7, 7)
    r_channel = roll_image(r_channel, -7, 7)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel)) # join layers
    show_image("after", img_BGRA)
    cv2.imwrite("rgb_rolled.png", img_BGRA)
    return img_BGRA
    
def main(args):
    args = ["cubes.jpg"]
    if not args:
        usage()
    else:
        file = args[0]
    rgb_roll(file)
    return True    
    
if __name__ == "__main__":
    path = script_path()
    main(sys.argv[1:])
    
    
    
    