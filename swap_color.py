#!/usr/bin/python3
from PIL import Image
import os
import sys
from itertools import product
from termcolor import colored

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def swap_color(image, swap='rgb'):
    im = Image.open(image)
    size = im.size
    imData = list(im.getdata())
    im2 = Image.new(im.mode, im.size)   #new png image
    colors = { 'r':0, 'g':1, 'b':2}
    c0 = colors[swap[0]]
    c1 = colors[swap[1]]
    c2 = colors[swap[2]]
    newData = [(item[c0], item[c1], item[c2]) for item in imData]
    im2.putdata(newData)
    fileName, fileType = file.split('.')
    fullName = fileName + "_" + swap + "." + fileType
    im2.save(fullName)
    print("image saved to: ", colored(fullName, "cyan"))

def usage(args):
    if not args or "-h" in args:
        print("Usage:")
        print("     <image> <rgb> (combination of 'r' + 'g' + 'b')")
        print("Example:")
        print("     python3 swap_color.py image.png gbr")
        sys.exit()
    else:
        if len(args) > 1:
            file = args[0]
            swap = args[1]
            if not os.path.exists(file):
                print("no such file: ", file)
                sys.exit()
            rgbComb = [''.join(i) for i in product("rgb", repeat=3)]
            if swap not in rgbComb:
                print("wrong combination of rgb")
                sys.exit()
            return file, swap
        else:
            print("not enough arguments")
            sys.exit()

if __name__ == "__main__":
    args = sys.argv[1:]
    file, swap = usage(args)
    path = script_path()
    swap_color(file, swap)
