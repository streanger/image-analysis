#!/usr/bin/python3
#calculating mean color value of image

from PIL import Image
import os
import sys
from termcolor import colored
import statistics
import numpy as np

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
    return meanRGB

if __name__ == "__main__":
    path = script_path()
    filename = "lamps.png"
    meanRGB = open_image(filename)
    print(meanRGB)
