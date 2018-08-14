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
        path = os.path.realpath(os.path.dirname(argv[0]))
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

def main(args):
    if not args:
        usage()

def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files


if __name__ == "__main__":
    main(sys.argv[1:])
