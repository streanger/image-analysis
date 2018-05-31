#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from PIL import Image

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def list_image_files(subpath=""):
    if not subpath:
        pass
    else:
        if not os.path.isdir(subpath):
            print("dir not exists:", subpath)
            return []
    path = script_path(subpath)
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    files = [item for item in files if not "pattern" in item]
    return files

if __name__ == "__main__":
    files = list_image_files()
    print("list of files in:", files)
    w,h=Image.open(files[0]).size
    N=len(files)
    arr=np.zeros((h,w,3),np.float)
    for im in files:
        imarr=np.array(Image.open(im),dtype=np.float)
        if len(imarr.shape) == 2:
            continue
            #skip greyscale images
        arr=arr+imarr/N
    # Round values in array and cast as 8-bit integer
    arr=np.array(np.round(arr),dtype=np.uint8)

    try:
        # Generate, save and preview final image
        out=Image.fromarray(arr,mode="RGB")
        out.save("Average.png")
        out.show()
        print("Image out: Average.png")
    except:
        print("Failed to create average image")





