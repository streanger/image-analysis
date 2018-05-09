import numpy as np
import cv2
import os
import sys
from PIL import Image

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def open_image(file):
    img = cv2.imread(file, 0)
    return img

def iter_files(files):
    for file in files:
        img = open_image(file)
        print(file, img.mean())
        gray = img
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cv2.imshow("image", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print("finished...")
    return True

def greyscale(files):
    for file in files:
        if "_grey" in file:
            continue
        fullPath = os.path.abspath(file)
        print(fullPath)
        img = open_image(fullPath)
        #cv2.imshow("image", img)
        #img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        outName = file.split('.')[0]+"_grey." + file.split('.')[1]
        print(outName)
        cv2.imwrite(outName, img)
    return True


if __name__ == "__main__":
    path = script_path()
    #files = [item for item in os.listdir() if "png" in item]
    #iter_files(files)
    #cv2.imshow("image", img)
    files = [item for item in os.listdir(path) if "png" in item]
    greyscale(files)
