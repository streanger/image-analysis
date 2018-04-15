#!/usr/bin/python3
#calculating mean color value of image

from PIL import Image
import os
import sys
from termcolor import colored
import statistics
import numpy as np
import random

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def open_image(file):
    im = Image.open(file)
    return im

def mean_color(filename):
    im = Image.open(filename)
    imData = list(im.getdata())
    #print(np.shape(imData))    #this is useful
    resizedData = np.resize(imData, (3, 241010))
    meanRGB = tuple([statistics.mean(item) for item in resizedData])
    return meanRGB

def ascii_list(n):
    l = ['.','-','~','"','^','*','&','$','@',chr(0x25a0)]
    return l[n]

def image_to_ascii(im):
    size = im.size
    imData = list(im.getdata())
    resized = np.resize(imData, size)
    print(resized, type(resized))
    dot = resized[10:14, 10:14]
    print(dot)
    picture= "_"*160 + "\n"
    print(picture)

def swap_color(im, swap='rgb'):
    size = im.size
    imData = list(im.getdata())
    im2 = Image.new(im.mode, im.size)   #new png image
    colors = { 'r':0, 'g':1, 'b':2}
    c0 = colors[swap[0]]
    c1 = colors[swap[1]]
    c2 = colors[swap[2]]
    newData = [(item[c0], item[c1], item[c2]) for item in imData]
    im2.putdata(newData)
    im2.save("new_image_" + swap + ".png")


if __name__ == "__main__":
    path = script_path()
    file = "lamps.png"
    im = open_image(file)
    image_to_ascii(im)
    print(ascii_list(9))
    #swap_color(im, swap='gbr')
