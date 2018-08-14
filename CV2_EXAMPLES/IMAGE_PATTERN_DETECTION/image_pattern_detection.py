#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt
from statistics import mean

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

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
    files = [item for item in files if not "pattern" in item]
    return files

def draw_chart(data):
    data_x = [key for key, val in enumerate(data)]
    plt.plot(data_x, data)
    plt.xlabel("pixels[n]")
    plt.ylabel("intensity[0-255]")
    plt.grid()
    plt.show()
    return True

def make_vector(someArray):
    #convert 2d, n-size array/matrix to 1d vector
    h = someArray.shape[0]
    someArray = someArray.flatten(1)
    return [mean(someArray[i:i+h]) for i in range(0,len(someArray),h)]

def make_hist(img, cx, cy):
    crop_img = img[cy-100:cy+100, cx-70:cx+70]
    cv2.imshow("crop_img", crop_img)
    hist = plt.hist(crop_img.ravel(),256,[2,254])
    plt.show()
    return True

if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        files = [args[0]]
        if not os.path.exists(files[0]):
            print("no such file:", files[0])
            sys.exit()
    else:
        files = list_image_files(subpath = "")  #"circles/"
    path = script_path()
    patterns = [item for item in os.listdir(path) if "pattern" in item and item.endswith(".png")]
    for file in files:
        if "front" in file or "-f" in args:
            pattern = patterns[1]
        else:
            pattern = patterns[0]
        img = cv2.imread(file)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgShape = img.shape[:2]

        template = cv2.imread(pattern, 0)
        w, h = template.shape[::-1]
        loc = []

        #decrease threshold to find pattern matching
        for x in range(55, 70)[::-1]:
            threshold = x/100
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            try:
                loc.count(0)
                pass
            except:
                break

        whiteLevel = 160
        #ellipse size
        ax1, ax2 = 70, 30
        axes = (ax1, ax2)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img_gray, "Main pattern", (pt[0]-20, pt[1]-10), font, 0.5, (255), 1, cv2.LINE_AA)
            if "front" in file or "-f" in args:
                #right ellipse
                #cx, cy = pt[0] + 305, pt[1] + 415
                cx, cy = pt[0] - 25, pt[1] - 85   #slim
                angle = 80
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                #rightMean = maskedImg[np.where(maskedImg>0)].mean()
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                #histogram
                #make_hist(maskedImg, cx, cy)


                #center ellipse
                #cx, cy = pt[0] + 150, pt[1] + 455
                cx, cy = pt[0] - 210, pt[1] - 65   #slim
                angle = 85
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)  #last arg -1 -> full
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)

                crop_01 = maskedImg[cy-50:cy-49, cx-100:cx+100]
                crop_02 = maskedImg[cy-1:cy+1, cx-100:cx+100]
                crop_03 = maskedImg[cy+49:cy+50, cx-100:cx+100]
                #cv2.imshow("crop01", crop_01)
                #cv2.imshow("crop02", crop_02)
                #cv2.imshow("crop03", crop_03)
                vect_01 = make_vector(crop_01)
                vect_02 = make_vector(crop_02)
                vect_03 = make_vector(crop_03)
                draw_chart(vect_01)
                draw_chart(vect_02)
                draw_chart(vect_03)

                #centerMean = maskedImg[np.where(maskedImg>0)].mean()
                centerWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                #histogram
                #make_hist(maskedImg, cx, cy)


                #left ellipse
                #cx, cy = pt[0] + 5, pt[1] + 515
                cx, cy = pt[0] - 380, pt[1] - 40     #slim
                angle = 80
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                #leftMean = maskedImg[np.where(maskedImg>0)].mean()
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                #histogram
                #make_hist(maskedImg, cx, cy)

                #print("mean values(left,center,right):", int(round(leftMean)), int(round(centerMean)), int(round(rightMean)))
                print("white pixels number(left,center,right):", leftWhiteNumber, centerWhiteNumber, rightWhiteNumber)
            else:
                #left ellipse
                #cx, cy = pt[0] - 330, pt[1] + 110
                cx, cy = pt[0] - 310, pt[1] - 120   #slim
                angle = 95
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1) 
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                #leftMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                #histogram
                #make_hist(maskedImg, cx, cy)


                #right ellipse
                #cx, cy = pt[0] - 175, pt[1] + 140
                cx, cy = pt[0] - 155, pt[1] - 130   #slim
                angle = 100
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1) 
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                #rightMean = maskedImg[np.where(maskedImg>0)].mean()
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                #histogram
                #make_hist(maskedImg, cx, cy)


                #print("mean values(left,right):", int(round(leftMean)), int(round(rightMean)))
                print("white pixels number(left,right):", leftWhiteNumber, rightWhiteNumber)
            break

        #find element
        if "front" in file or "-f" in args:
            resistor = "element.png"
            resistorTemp = cv2.imread(resistor, 0)
            w, h = resistorTemp.shape[::-1]
            res = cv2.matchTemplate(img_gray, resistorTemp, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 1)
                print("Element:True")
                break
            else:
                print("Element:False")

        if "-p" in args:
        #if 1:
            cv2.imshow('Detected',img_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

