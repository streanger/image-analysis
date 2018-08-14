#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from PIL import Image

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def open_image(file, color=True):
    if color:
        img = cv2.imread(file, 1)   #read in color mode
    else:
        img = cv2.imread(file, 0)   #read in grayscale mode
    return img

def iter_files(files):
    for file in files:
        img = open_image(file, color=False)
        #print(file, img.mean())
        gray = img
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)   #threshold
        cv2.imshow("image", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print("finished...")
    return True

def greyscale(files):
    for file in files:
        if "_grey" in file:
            continue #do not repeat greyscale
        fullPath = os.path.abspath(file)
        img = open_image(fullPath, color=False)
        outName = file.split('.')[0] + "_grey." + file.split('.')[1]
        print("file out: ", outName)
        cv2.imwrite(outName, img)
    return True

def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg", ".gif")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-h" in args:
        print("convert images to greyscale. Usage:")
        print("     <script>            <--- convert all images in current dir")
        print("     <script> <file>     <--- convert specified file")
        print("     <script> -h         <--- show this help")
        sys.exit()
    if args:
        file = args[0]
        if os.path.isfile(file):
            files = [file]
        else:
            print("no such file")
            sys.exit()
    else:
        files = list_image_files()
    greyscale(files)
    #iter_files(files)
