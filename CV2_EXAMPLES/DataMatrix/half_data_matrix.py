#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
from statistics import mean
import matplotlib.pyplot as plt
import time
import math
import imutils

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(argv[0]))
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

def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    return files

def find_pattern(image, pattern):
    template = cv2.imread(pattern, 0)
    try:
        w, h = template.shape[::-1]
    except:
        print("0 0 0\ntemplate error in pattern:", pattern)
        exit()
    loc = []
    patternTemp = cv2.imread(pattern, 0)
    w, h = patternTemp.shape[::-1]
    res = cv2.matchTemplate(image, patternTemp, cv2.TM_CCOEFF_NORMED)
    threshold = 0.92
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (155,255,155), 2)
        #show_image("pattern", image)
        return pt
    else:
        return False   #if not found

def binary_image(img):
    img_gray = img      #make sure u use grayscale image
    (thresh, im_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return im_bw

def gaussian_thres(img):
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,255,50)
    return thresh

def blur_image(img):
    blur = cv2.blur(img,(2,2))
    return blur

def calc_dist(p1, p2):
    distance = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(0.5)
    return distance

def longest_pair(pairs):
    distances = [(p, calc_dist(p[0],p[1])) for p in pairs]
    return max(distances, key=lambda x:x[1])

def draw_chart(data):
    data_x = [key for key, val in enumerate(data)]
    plt.plot(data_x, data)
    plt.xlabel("pixels[n]")
    plt.ylabel("intensity[0-255]")
    plt.grid()
    plt.show()
    return True

def make_vector(someArray, slim=1):
    #convert 2d, n-size array/matrix to 1d vector
    h = someArray.shape[0]
    if (slim*2) >= h:
        print("slim val is too much. Slim: {}, h: {}".format(slim, h))
        sys.exit()
    someArray = someArray.flatten(1)
    #return [mean(someArray[i:i+h]) for i in range(0,len(someArray),h)]
    return [mean(someArray[i+slim:i+h-slim]) for i in range(0,len(someArray),h)]     #reduced

def mean_list(data, n, dots=18, slim=0):
    out = []
    for x in range(dots):
        p1 = int(round(x*n))
        p2 = int(round((x+1)*n))
        #out.append(int(round(mean(data[p1+slim:p2-slim]))))
        val = mean(data[p1+slim:p2-slim])
        if val > 240:
            out.append(1)
        else:
            out.append(0)
    #out = [int(round(mean(data[x+slim:x+n-slim]))) for x in range(0, len(data), n)]
    return out

def main(args):
    #if not args:
    #    usage()
    if args:
        file = args[0]
    else:
        file = "data1.jpg"
    img = cv2.imread(file, 0)
    imgColor = cv2.imread(file, 1)
    for x in range(1):
        img = blur_image(img)
    #im_bw = binary_image(img)
    gauss = gaussian_thres(img)
    #show_image("binary", im_bw)
    #show_image("gauss", gauss)
    #h, w = img.shape

    gray = img
    edges = cv2.Canny(img,250,250,apertureSize = 3)
    minLineLength = 100
    maxLineGap = 20
    #lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    lines = cv2.HoughLinesP(edges,1,np.pi/250,340,minLineLength,maxLineGap)
    for key, line in enumerate(lines[:2]):
        for x1,y1,x2,y2 in line:
            cv2.line(imgColor,(x1,y1),(x2,y2),(150,255,150),2)
        p1 = (x1, y1)
        p2 = (x2, y2)
        if key == 0:
            alfa1 = (math.asin((y1-y2)/calc_dist(p1, p2)))/math.pi*180
            line1 = (x1,y1,x2,y2)
        elif key == 1:
            alfa2 = (math.asin((y1-y2)/calc_dist(p1, p2)))/math.pi*180
            line2 = (x1,y1,x2,y2)

    #consider rotating image, find lines again, and then crop


    #crop matrix
    p1, p2 = line1[:2], line1[2:4]
    p3, p4 = line2[:2], line2[2:4]
    longest = longest_pair(((p1, p3), (p1, p4), (p2, p3), (p2, p4)))
    #points = sum(longest[0], ())      #flatten tuples
    points = longest[0]
    dist1 = int(round(calc_dist(p1, p2)))
    dist2 = int(round(calc_dist(p3, p4)))
    
    if points[0][1] < points[1][1]:
        pStart, pStop = points
    else:
        pStop, pStart = points
    #crop_img = gauss[y1:y2, x1:x2]
    crop_img = gauss[pStart[1]:pStart[1]+dist2, pStart[0]:pStart[0]+dist1]
    #show_image("crop_image", crop_img)         #extracted image
    dots = 18
    
    h, w = crop_img.shape
    ySize = h/dots
    xSize = w/dots
    #print("xSize:", xSize)
    #print("w: {}, h: {}".format(w, h))

    slimY = 5
    #analysis of vectors
    dataMatrix = []
    for x in range(dots):
        #ySize = crop_img.shape[0]/18
        y1 = int(round(ySize*x)) + slimY
        y2 = y1 + int(round(ySize)) - 2*slimY
        crop = crop_img[y1:y2, 0:w]
        #show_image("crop_image", crop)
        vect = make_vector(crop, 0)
        #print(vect)
        draw_chart(vect)
        data = mean_list(vect, xSize, dots=dots, slim=5)
        dataMatrix.append(data)
        print(data)
    #print(dataMatrix)


if __name__ == "__main__":
    begin = time.time()
    main(sys.argv[1:])
    print("elapsed:", time.time() - begin)
