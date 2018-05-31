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

def open_image(file, color=True):
    if color:
        img = cv2.imread(file, 1)   #read in color mode
    else:
        img = cv2.imread(file, 0)   #read in grayscale mode
    return img

def threshold_image(img):
    ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY)   #threshold
    cv2.imshow("image threshold", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def write_as_greyscale(file):
    if "_grey" in file:
        return False
    img = cv2.imread(file, 0)
    outName = file.split('.')[0] + "_grey." + file.split('.')[1]
    cv2.imwrite(outName, img)
    return True

def greyscale(file):
    img = open_image(file, color=False)
    return img

def write_image(img, name, extension=".png"):
    if not extension in (".png", "jpeg", "jpg"):
        return False
    outName = name + extension
    cv2.imwrite(outName, img)
    return True

def list_image_files(subpath):
    if not subpath:
        pass
    else:
        if not os.path.isdir(subpath):
            print("dir not exists:", subpath)
            return []
    path = script_path(subpath)
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

def find_circle(file):
    img = greyscale(file)
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=30)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),2)
    cv2.imshow("circles --> " + file, cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def read_colors(img):
    b = img[:,:,0]
    img[:,:,0] = 55
    #img[:,:,1] = 155
    #img[:,:,2] = 255
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def watermark_image(img, mark):
    dst = cv2.addWeighted(img, 0.2, mark, 0.8, 0)
    cv2.imshow("watermarked image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def image_inpainting(img, mask):
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def object_tracking(img, level=()):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    if not level:
        lower_val = np.array([70,100,100])       #([110,50,50])
        upper_val = np.array([130,255,255])    #([130,255,255])
    else:
        lower_val = level[0]
        upper_val = level[1]
    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_and(img, img, mask=mask)  #this is useful
    cv2.imshow('hsv', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    files = list_image_files(subpath = "")  #"circles/"
    red = (np.array([0,50,50]),
            np.array([30,255,255]))
    green = (np.array([35,50,50]),
            np.array([70,255,255]))
    blue = (np.array([90,50,50]),
            np.array([125,255,255]))
    black = (np.array([0,0,0]),
            np.array([255,255,200]))
    silver = (np.array([0,0,100]),
            np.array([255,255,255]))

    pattern = "pattern.png"
    template = cv2.imread(pattern, 0)
    w, h = template.shape[::-1]
    for file in files:
        #find_circle(file)
        img = cv2.imread(file)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        #pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        #pts = pts.reshape((-1,1,2))
        #cv2.polylines(img,[pts],True,(0,255,255))
        for pt in zip(*loc[::-1]):
            #print(pt)
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 1)
            #pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
            pts = np.array([[pt[0]-40,pt[1]+600],
                            [pt[0]+60,pt[1]+580],
                            [pt[0]+50,pt[1]+430],
                            [pt[0]-80,pt[1]+480]],
                            np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(img,[pts],True,(0,255,255))
            #crop_img = img[pt[0]+1:pt[0], pt[1]:pt[1]+1]
            #crop_img = img[pt[0]-350:pt[0]+500, pt[1]+170:pt[1]+800]
            #cv2.imshow("cropped", crop_img)

            cv2.rectangle(img, (pt[0] + 265, pt[1] + 338), (pt[0] + 356, pt[1] + 464), (255,150,0), 1)
            cv2.rectangle(img, (pt[0] + 90, pt[1] + 390), (pt[0] + 200, pt[1] + 520), (255,150,0), 1)
            cv2.rectangle(img, (pt[0] - 66, pt[1] + 450), (pt[0] + 64, pt[1] + 580), (255,150,0), 1)
            break
        cv2.imshow('Detected',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
