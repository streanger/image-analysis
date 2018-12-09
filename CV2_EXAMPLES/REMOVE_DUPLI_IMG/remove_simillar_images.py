#!/usr/bin/python3
import sys
import os
import re
import shutil
import numpy as np
import cv2

def script_path(subpath=""):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def usage():
    print("-> script for searching for duplicates of image")
    print("-> duplicates will be found and moved to new dir")
    print("-> usage example:")
    print("\tremove_dupli.py    some_image.png")
    input("-> press enter to exit... ")
    return True
    
def find_threshold_value(filename):
    value = re.findall("\d+\.\d+", filename)
    threshold = 0.9
    try:
        value = float(value[0])
        if value > 0 and value < 1:
            threshold = value
    except:
        pass
    return threshold
    
def list_images():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files
    
def move_file(file, currentPath, newPath):
    currentFilePath = os.path.join(currentPath, file)
    newFilePath = os.path.join(newPath, file)
    shutil.move(currentFilePath, newFilePath)
    return True
    
def check_pattern(file, pattern, threshold=0.9):
    img = cv2.imread(file, 0)
    res = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        print("Pattern found in: <{}>".format(file))
        return True
    else:
        print("No pattern in: <{}>".format(file))
        return False
        
def main(args):
    currentPath = script_path()
    
    # create dir for duplicates
    newDir = "dupli"
    newPath = os.path.join(currentPath, newDir)
    if not os.path.exists(newDir):
        os.makedirs(newDir)
        
    # read pattern to memory
    try:
        patternFile = args[0]
        threshold = find_threshold_value(sys.argv[0])
        pattern = cv2.imread(patternFile, 0)
    except:
        usage()
        return False
        
    # list images & search for duplicates
    files = list_images()
    for file in files:
        status = check_pattern(file, pattern, threshold)
        if status:
            move_file(file, currentPath, newPath)
    return True
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
