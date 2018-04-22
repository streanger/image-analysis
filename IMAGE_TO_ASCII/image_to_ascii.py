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

def ascii_list(n):
    l = [' ',' ','.','`',',','-','-','~','"','^','*',';','i','l','=','v','x','C','P','G','&','$','O','Q','@','@','X','X','#','#',chr(0x25a0),chr(0x25a0)]   #32
    l = list("".join([item*8 for item in l]))
    #l = l[::-1]
    l = l[::]
    return l[n]

def image_to_ascii(file, printIm=True):
    #picture= "_"*160 + "\n"
    resolution = 0.5
    picture = ""
    if 1:
        im = Image.open(file)  #with PIL
        imSize = im.size
        data = list(im.getdata())
        #data = data[::-1]
        #print(data)
        #print("before:\n", data[600:900])
        if not type(data[0]) is int:
            data = [statistics.mean(item[:3]) for item in data]
        #print("after:\n", data[600:900])
        #input()
        imData = np.resize(data, imSize)
        size = imData.shape
        resized = np.resize(imData, (imSize[1], imSize[0]))
        size = resized.shape
    else:
        imData = np.matrix(range(14400))
        resized = np.resize(imData, (120, 120))
        size = resized.shape
    #dotSizeY = size[0]//50 #+ 1  #change it to resize in x i y axes
    dotSizeY = size[0]//round(64*resolution)  #+ 1  #change it to resize in x i y axes  64/120
    if dotSizeY == 0:
        dotSizeY +=1
    #dotSizeX = size[1]//80 #+ 1
    dotSizeX = size[1]//round(120*resolution) #+ 1
    if dotSizeX == 0:
        dotSizeX +=1
    #dotsNoX = size[0]//dotSizeX +1
    dotsNoX = size[1]//dotSizeX +1
    #dotsNoY = size[1]//dotSizeY +1#+1
    dotsNoY = size[0]//dotSizeY +1#+1
    print("dotsNo, x,y:", dotsNoX, dotsNoY, size)
    #resize matrix to full dots in botx X and Y axes!!! important
    print("sizeX, should be:", dotSizeX*dotsNoX)
    print("sizeY, should be:", dotSizeY*dotsNoY)
    zeroM = np.zeros((dotSizeY*dotsNoY, dotSizeX*dotsNoX))
    #zeroM[:,:-1*(dotSizeX*dotsNoX - size[0])] = resized   #append column   #think about that
    print(zeroM.shape)
    #print(resized.tolist())
    #print()
    lines = []
    counter = 0
    for y in range(dotsNoY):
        line = []
        for x in range(dotsNoX):
            dot = resized[y*dotSizeY:(y+1)*dotSizeY, x*dotSizeX:(x+1)*dotSizeX]
            #dot = resized[x*dotSizeX:(x+1)*dotSizeX, y*dotSizeY:(y+1)*dotSizeY]
            #print(dot)
            counter +=1
            if dot == []:
                dot = [0]
            try:
                #val = int(np.mean(dot)//10)
                val = int(np.mean(dot))
            except:
                val = 1
            line.append(val)
            picture += ascii_list(val)
        lines.append(line)
        picture += "\n"
    m = np.matrix(lines)
    m = m - m.min()
    print(m.tolist())
    print(m.shape)
    #m = np.resize(m, (45,45))
    #print(m.shape)
    #print(m.min(), m.max())
    #m = m.tolist()  #use this
    #m = m.flatten().tolist()[0]    #uncomment this one
    if  m.max() == 1:
        m = m*255
    m = m.flatten().tolist()[0]
    #for index, item in enumerate(m):
    #    print(ascii_list(item), end="")
    #    if index%(int(sys.argv[4])) == 0:
    #        print()
    #print()
    #sys.exit()
    #print(m)
    #print(m)
    #m = np.swapaxes(m, 1, 0)   #uncomment here to turn photo 90deg
    #print("\n"*2, m)
    #for line in m:
        #print(line)
        #for item in line:
            #print(item)
            #print(ascii_list(item), end="")
            #pass
        #print()
    if printIm:
        picture = picture.replace("\n","")
        picture = list(picture)
        #print(picture[:100])
        #picture = rotate_list(picture, 500)
        #print(picture[:100])
        picture = "".join(picture)
        #print(picture)
    if len(sys.argv)>3:
        correction = sys.argv[3]
    else:
        correction = 0
    for index, item in enumerate(picture):
        if index%(dotsNoX-1*int(correction)) == 0:
            print()
        print(item, end="")
    print()

def rotate_list(l, n):
    return l[-n:] + l[:-n]

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

def usage():
    print("Example of usage:")
    print("     <some_file> <print_ascii_image> <correction_number>")
    print("     image.png -p 0")
    sys.exit()

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        usage()
    path = script_path()
    file = args[0]
    if "-p" in args:
        printIm = True
    else:
        printIm = False
    image_to_ascii(file, printIm)
    #swap_color(im, swap='gbr')
