#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def cat_images(file1, file2, axisVal, write=True):
    img1 = cv2.imread(file1)
    img2 = cv2.imread(file2)
    if axisVal not in (0, 1):
        print("wrong axis. Choose 0 (for vertically) or 1 (for horizontally)")
        sys.exit()
    vis = np.concatenate((img1, img2), axis=axisVal)
    cv2.imwrite("out.png", vis)
    return True

def usage():
    print("Usage:")
    print("    python [cat_images.py] [file1] [file2] [-v]")
    print("    file1, file2 - files to concatenate")
    print("    [-v] -merge vertically; with no argument merge horizontally")
    #sys.exit()

def main(args):
    path = script_path()
    if not args:
        usage()
        files = [item for item in os.listdir(path) if item.split(".")[-1].lower() in ("png", "jpeg", "jpg")][:2]
        if not len(files) == 2:
            sys.exit()
    else:
        if len(args) > 1:
            files = args[:2]
        else:
            sys.exit()
    for file in files:
        if not os.path.exists(file):
            print("no such file:", file)
            sys.exit()
    if "-v" in args:
        axis = 0
    else:
        axis = 1
    cat_images(files[0], files[1], axis, write=True)


if __name__ == "__main__":
    main(sys.argv[1:])

