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
        print("elapsed time: {}s".format(after-before))
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
    print("put help content here...\n")
    sys.exit()

def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

@timer
def main(args):
    args = ['test_image.png']
    if not args:
        usage()
    file = args[0]
    #print(file)
    img = cv2.imread(file, 0)       #read in greyscale
    blur = cv2.blur(img, (3, 3))    #blur the image to reduce noise
    ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
    #show_image('test_image', img)
    #show_image('thresh', thresh)
    
    #find contours
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    #show_image('contours img', im2)
    
    #find convex hull
    hull = []
    for key, contour in enumerate(contours):
        hull.append(cv2.convexHull(contour, False))

    #print("hull:", type(hull), len(hull))
    #draw hull    
    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
     
    # draw contours and hull points
    for key, contour in enumerate(contours):
        color_contours = (0, 255, 0) # green - color for contours
        color = (255, 0, 0) # blue - color for convex hull
        # draw ith contour
        cv2.drawContours(drawing, contours, key, color_contours, 1, 8, hierarchy)
        # draw ith convex hull object
        cv2.drawContours(drawing, hull, key, color, 1, 8)
    
    show_image('hull image', drawing)    
        
if __name__ == "__main__":
    path = script_path()
    main(sys.argv[1:])
    
    
    
    
    
    