#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
import math
import time
from statistics import mean

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def file_exists(file):
    if not os.path.exists(file):
        print("no such file:", file)
        sys.exit()

def save_file(file, image):
    imgDir = "analysed"
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    path = os.path.join(imgDir, file)
    cv2.imwrite(path, image)
    return True

def usage():
    print("put help content here...\n")
    sys.exit()
    
def resize_image(img, newSize):
    height = round((img.shape[0])*(newSize/100))
    width = round((img.shape[1])*(newSize/100))
    resized = cv2.resize(img, (width, height))
    return resized
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def make_dir(new_dir):
    ''' make new dir, switch to it and return new path '''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path
    
def roll_image(img, x_axis, y_axis):
    img = np.roll(img, y_axis, axis=0)   # axis: 0-up-down, 1-right-left
    img = np.roll(img, x_axis, axis=1)   # axis: 0-up-down, 1-right-left
    return img
    
def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

def rgb_roll(image, deg, radius):
    ''' todo: set parameters to roll: rotation & radius (R-G-B are set between 120 deg) '''
    dictio = convert_rotation(deg, radius)
    # print(dictio)
    # image = cv2.imread(file)
    # show_image("before", image)
    b_channel, g_channel, r_channel = cv2.split(image)      # split to R-G-B
    b_channel = roll_image(b_channel, dictio['B_a'], dictio['B_b'])                # move each one
    g_channel = roll_image(g_channel, dictio['G_a'], dictio['G_b'])
    r_channel = roll_image(r_channel, dictio['R_a'], dictio['R_b'])
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel)) # join layers
    # img_BGRA = resize_image(img_BGRA, 25)
    # show_image("after", img_BGRA)
    # subpath = make_dir("rolled")
    # outFile = "out{}.png".format(str(deg).zfill(4))     # use it to create gif or video, otherwise just 'out.png'
    # outFile = os.path.join(subpath, outFile)
    # cv2.imwrite(outFile, img_BGRA)
    return img_BGRA

def convert_rotation(deg, radius):
    # R layer
    R_a = math.cos((deg/360)*2*math.pi)*radius
    R_b = math.sin((deg/360)*2*math.pi)*radius
    # G layer
    G_a = math.cos(((deg+120)/360)*2*math.pi)*radius
    G_b = math.sin(((deg+120)/360)*2*math.pi)*radius
    # B layer
    B_a = math.cos(((deg+240)/360)*2*math.pi)*radius
    B_b = math.sin(((deg+240)/360)*2*math.pi)*radius
    dictio = {"R_a":R_a,
              "R_b":R_b,
              "G_a":G_a,
              "G_b":G_b,
              "B_a":B_a,
              "B_b":B_b}
    dictio = dict(zip(dictio.keys(), [round(item) for item in list(dictio.values())]))
    return dictio

def create_animation(file):
    radius = 0
    for deg in range(180):
        # deg, radius = [int(item.strip()) for item in input("put deg, radius: ").split(',')]
        if deg < 90:
            radius += 0.75
        else:
            radius -= 0.75
        rgb_roll(file, deg*2, radius)
    return True
    
def main(args):
    args = ["cubes.jpg"]
    if not args:
        usage()
    else:
        file = args[0]
    create_animation(file)
    return True   
    
if __name__ == "__main__":
    path = script_path()
    # main(sys.argv[1:])
    rgb_roll("cubes.jpg", 45, 5)
    
    
    
    