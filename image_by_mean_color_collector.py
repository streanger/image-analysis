#!/usr/bin/python3
#collecting images(.png) in current dir, by meany color

from PIL import Image
import os
import sys
from termcolor import colored
import statistics
import numpy as np
from shutil import copyfile

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def open_image(filename):
    im = Image.open(filename)
    #args = [item for item in dir(im) if (not "__" in item) and (not item[0] == "_")]
    imData = list(im.getdata())
    #print(np.shape(imData))    #this is useful
    resizedData = np.resize(imData, (3, 241010))
    meanRGB = tuple([statistics.mean(item) for item in resizedData])
    #return meanRGB
    return statistics.mean(meanRGB)

def make_dir(dirName="REPLACED"):
    path = script_path()
    path = os.path.join(path, dirName)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            print("error while making new dir...")
            sys.exit()
    return path

if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        meanColor = args[0]
    else:
        meanColor = 127
    path = script_path()
    filesPng = [item for item in os.listdir(path) if item[-4:] == ".png"]
    #file = "lamps.png"
    make_dir("LIGHT")
    make_dir("DARK")
    for file in filesPng:
        meanRGB = open_image(file)
        if meanRGB < meanColor:
            subPath = os.path.join(path, "DARK")
            colorType = "DARK"
        else:
            subPath = os.path.join(path, "LIGHT")
            colorType = "LIGHT"
        subPath = os.path.join(subPath, file)
        print(file, meanRGB, colorType)
        copyfile(file, subPath)
