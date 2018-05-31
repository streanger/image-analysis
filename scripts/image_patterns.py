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
    files = [item for item in files if not "solder" in item]
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

def object_tracking(file, level=""):
    levels = {}
    levels["red"] = (np.array([0,50,50]), np.array([30,255,255]))
    levels["green"] = (np.array([50,60,60]), np.array([70,255,255]))
    levels["blue"] = (np.array([90,50,50]), np.array([125,255,255]))
    #levels["black"] = (np.array([0,0,0]), np.array([255,255,200]))
    #levels["silver"] = (np.array([0,0,100]), np.array([255,255,255]))

    img = cv2.imread(file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    if not level:
        lower_val = np.array([70,100,100])       #([110,50,50])
        upper_val = np.array([130,255,255])    #([130,255,255])
    else:
        lower_val = levels[level][0]
        upper_val = levels[level][1]
    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_and(img, img, mask=mask)  #this is useful

    #res = cv2.GaussianBlur(res,(5,5),0)
    res = cv2.medianBlur(res,5)
    res = cv2.medianBlur(res,5)


    
    #draw contours of objects
    img_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,40,255,0)
    contours,hierarchy,some = cv2.findContours(thresh, 2, 1)
    cnt = contours[0]
    #M = cv2.moments(cnt)
    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    #area = cv2.contourArea(cnt)
    #print(area)
    


    '''
    #removing small objects on mask
    img_bw = 255*(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')
    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (200,200))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)
    #mask = np.dstack([mask, mask, mask]) / 255
    #out = img * mask
    res = cv2.bitwise_and(img, img, mask=mask)  #this is useful
    '''
    
    cv2.imshow('level [%s] in [%s]' % (level, file), res)
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

    patterns = [item for item in os.listdir() if "solder" in item and item.endswith(".png")]
    print(patterns)
    #sys.exit()
    #pattern = "pattern.png"
    #template = cv2.imread(pattern, 0)
    #w, h = template.shape[::-1]
    for file in files:
        img = cv2.imread(file)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        #cl1 = clahe.apply(img_gray)
        #cv2.imshow('Contrast in %s' % (file), cl1)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        #object_tracking(file, level="red")
        #object_tracking(file, level="green")
        #object_tracking(file, level="blue")
        #object_tracking(file, level="black")
        #object_tracking(file, level="silver")


        '''
        pattern = "resistor.png"
        template = cv2.imread(pattern, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6 #0.6 for resistor
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            #print(pt)
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            break
        cv2.imshow('Detected [%s] in %s' % (pattern, file), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''


        patternFound = False
        for pattern in patterns:
            template = cv2.imread(pattern, 0)
            w, h = template.shape[::-1]
            try:
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            except:
                break
            threshold = 0.6 #0.6 for resistor
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                #print(pt)
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
                #patternFound = True
                #break
            cv2.imshow('Detected [%s] in %s' % (pattern, file), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            if patternFound:
                break


        
