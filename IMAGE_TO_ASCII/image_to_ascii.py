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
    l = ['.','-','~','"','^','*','&','$','@', chr(0x25a0)]
    l = l[::]
    return l[n]

def image_to_ascii(im):
    picture= "_"*160 + "\n"
    size = im.size
    imData = list(im.getdata())
    resized = np.resize(imData, size)
    #print(resized, type(resized))
    #dot = resized[10:14, 10:14]
    dotSize = size[0]//160 + 1
    dotsNoX = size[1]//dotSize  # +1
    print(dotSize, size)
    lastDotX = size[0]%dotSize  #do the same with Y
    dotsNoY = size[0]//dotSize  # +1
    lines = []
    for y in range(dotsNoY):
        line = []
        for x in range(dotsNoX):
            dot = resized[y*dotSize:(y+1)*dotSize, x*dotSize:(x+1)*dotSize]
            #print(dot, (x+1)*dotSize)
            val = int(np.mean(dot)//25)
            #val = np.mean(dot)
            line.append(val)
            picture += ascii_list(val-1)
            #print((np.mean(dot)*10)//255, end=" ")
        lines.append(line)
        picture += "\n"
        #print()
    #print(lines)
    m = np.matrix(lines)
    print(m.min(), m.max())
    #print(dot, dotSize)
    #print(dotsNoY)
    #print(len(picture))
    #print(picture)

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
    args = sys.argv[1:]
    path = script_path()
    #file = "lamps.png"
    file = "chess.png"
    file = args[0]
    im = open_image(file)
    image_to_ascii(im)
    #swap_color(im, swap='gbr')
