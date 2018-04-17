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
    l = [' ','`','.',',','-','~','"','^','*',';','i','l','v','x','p',']','C','P','G','&','$','@','@','#','#',chr(0x25a0),chr(0x25a0)]
    l = l[::]
    return l[n]

def image_to_ascii(file, printIm=True):
    picture= "_"*160 + "\n"
    if 1:
        im = Image.open(file)
        imSize = im.size
        #data = (np.resize(list(im.getdata()), (44,44))).tolist()
        data = list(im.getdata())
        #print('\n', data)
        data = [statistics.mean(item[:3]) for item in data]
        #print('\n'*2, data)
        #print(data)
        #sys.exit()
        imData = np.resize(data, imSize)
        #imData = np.matrix(list(im.getdata()))
        #print(imData.tolist())
        size = imData.shape
        #print("size:", size)
        resized = np.resize(imData, imSize)
        size = resized.shape
        #print("size:", size)
        #sys.exit()
    else:
        #example data
        imData = np.matrix(range(192))
        resized = np.resize(imData, (12, 16))
        size = resized.shape
        #print(resized)
    #im2 = Image.new(im.mode, im.size)   #new png image
    #resized = resized.tolist()
    #im2.putdata(resized)
    #im2.save("new_file.png")


    #print(resized, type(resized))
    #dot = resized[10:14, 10:14]
    dotSize = size[0]//60 + 1
    #dotSize = size[0]//160 + 1
    dotsNoX = size[0]//dotSize +1
    #print("size:{0}, dotSize:{1}".format(size, dotSize))
    #lastDotX = size[0]%dotSize  #do the same with Y
    dotsNoY = size[1]//dotSize -1#+1
    #print("dotsNoY, X:", dotsNoY, dotsNoX)
    lines = []
    dotsNo = (size[0]*size[1])//dotSize
    #print("\n", dotsNo)
    #sys.exit()
    for y in range(dotsNoY):
        line = []
        for x in range(dotsNoX):
            #dot = resized[x*(dotSize):(x+1)*dotSize, y*dotSize:(y+1)*dotSize]
            #dot = resized[y*dotSize:(y+1)*dotSize, y*dotSize:(y+1)*dotSize]
            #dot = resized[x*dotSize:(x+1)*dotSize, x*dotSize:(x+1)*dotSize]
            dot = resized[y*dotSize:(y+1)*dotSize, x*dotSize:(x+1)*dotSize]
            try:
                val = int(np.mean(dot)//10)
            except:
                val = 0
            #print(dot, val)
            #val = np.mean(dot)
            line.append(val)
            #picture += ascii_list(val)
            #print((np.mean(dot)*10)//255, end=" ")
        lines.append(line)
        picture += "\n"
    m = np.matrix(lines)
    m = m - m.min()
    #print(m.min(), m.max())
    m = m.tolist()
    #m = np.swapaxes(m, 1, 0)   #uncomment here to turn photo 90deg
    #print("\n"*2, m)
    for line in m:
        #print(line)
        for item in line:
            #print(item)
            print(ascii_list(item), end="")
        print()
    if printIm:
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
    args = sys.argv[1:]
    path = script_path()
    #file = "lamps.png"
    file = "chess.png"
    file = args[0]
    if "-p" in args:
        printIm = True
    else:
        printIm = False
    #im = open_image(file)
    image_to_ascii(file, printIm)
    #swap_color(im, swap='gbr')
