#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
import shutil

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def save_file(file, image):
    imgDir = "duplicates"
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    path = os.path.join(imgDir, file)
    cv2.imwrite(path, image)

def list_photos():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

def move_file(file, pattern):
    #read file to image
    pass
    img = cv2.imread(file, 0)
    res = cv2.matchTemplate(img, pattern, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
        print("Pattern found in image:", file)
        currentFilePath = os.path.join(path, file)
        newFilePath = os.path.join(newPath, file)
        shutil.move(currentFilePath, newFilePath)
        break
    else:
        print("No pattern in image:", file)


if __name__ == "__main__":
    path = script_path()
    newDir = "dupli"
    newPath = os.path.join(path, newDir)
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    patternFile = "pattern.png"
    pattern = cv2.imread(patternFile, 0)
    w, h = pattern.shape[::-1]
    files = list_photos()
    for file in files:
        print(file)
        move_file(file, pattern)







