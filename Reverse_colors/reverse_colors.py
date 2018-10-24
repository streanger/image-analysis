#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from statistics import mean

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
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
    return True

def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def reverse_colors(img):
    ''' both ways should work '''
    reversed = cv2.bitwise_not(img)
    # reversed = (255-img)
    return reversed
    
def main(args):
    if not args:
        usage()
        sys.exit()
    else:
        file = args[0]
    img = cv2.imread(file)
    # show_image("normal", img)
    reversed = reverse_colors(img)
    # show_image("reversed", reversed)
    cv2.imwrite("_reversed.".join(file.split('.')), reversed)
    return True
    
def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files


if __name__ == "__main__":
    path = script_path()
    main(sys.argv[1:])
