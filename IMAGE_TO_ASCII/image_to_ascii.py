#!/usr/bin/python3
#calculating mean color value of image

from PIL import Image
import os
import sys
from termcolor import colored
import statistics
import numpy as np
import random
import matplotlib.image as img
import scipy


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

def ascii_list():
    l = [' ',' ','.','`',',','-','-','~','"','^','*',';','i','l','=','v','x','C','P','G','&','$','O','Q','@','@','X','X','#','#',chr(0x25a0),chr(0x25a0)]   #32
    l = list("".join([item*8 for item in l]))
    #reverse list means reversed colors
    #return l[::-1]
    return l

def image_to_ascii(file, printIm=True, reverseColor=False):
    asciiList = ascii_list()
    if reverseColor:
        asciiList = asciiList[::-1]
    resolution = 1.25
    picture = ""
    if 1:
        im = Image.open(file)  #with PIL
        imSize = im.size
        data = list(im.getdata())
        if not type(data[0]) is int:
            data = [statistics.mean(item[:3]) for item in data]
        imData = np.resize(data, imSize)
        size = imData.shape
        resized = np.resize(imData, (imSize[1], imSize[0]))
        if resized.max() == 1:
            resized *= 255
        size = resized.shape
    else:
        imData = np.matrix(range(14400))
        resized = np.resize(imData, (120, 120))
        size = resized.shape
    dotSizeY = size[0]//round(50*resolution)  #+ 1  #change it to resize in x i y axes  64/120
    #dotSizeY = size[1]//round(64*resolution)  #+ 1  #change it to resize in x i y axes  64/120
    if dotSizeY == 0:
        dotSizeY +=1
    dotSizeX = size[1]//round(80*resolution) #+ 1
    #dotSizeX = size[0]//round(120*resolution) #+ 1
    if dotSizeX == 0:
        dotSizeX +=1
    dotsNoX = size[1]//dotSizeX
    dotsNoY = size[0]//dotSizeY
    #resize matrix to full dots in botx X and Y axes!!! important
    #print("dotsNo, x,y:", dotsNoX, dotsNoY, size)
    #print("sizeX, should be:", dotSizeX*dotsNoX)
    #print("sizeY, should be:", dotSizeY*dotsNoY)
    lines = []
    counter = 0
    for y in range(dotsNoY):
        line = []
        for x in range(dotsNoX):
            dot = resized[y*dotSizeY:(y+1)*dotSizeY, x*dotSizeX:(x+1)*dotSizeX]
            #print(dot)
            counter +=1
            if dot == []:
                dot = [0]
            try:
                val = int(np.mean(dot))
            except:
                val = 1
            line.append(val)
            picture += asciiList[val]
        lines.append(line)
        picture += "\n"
    #print(picture)  #will pring picture on screen
    return picture

def rotate_list(l, n):
    return l[-n:] + l[:-n]

def swap_color(file, swap='rgb'):
    im = Image.open(file)
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

def usage():
    print("Example of usage:")
    print("     <some_file> <print_ascii_image>")
    print("     image.png -p")
    sys.exit()
    #put as parameter: resolution and reverseColor

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        usage()
    path = script_path()
    file = args[0]
    image = image_to_ascii(file, reverseColor=False)
    print(colored(image, "cyan"))
