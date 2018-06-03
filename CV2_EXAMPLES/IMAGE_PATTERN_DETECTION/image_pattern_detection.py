#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys

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


if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        files = [args[0]]
        if not os.path.exists(files[0]):
            print("no such file:", files[0])
            sys.exit()
    else:
        files = list_image_files(subpath = "")  #"circles/"
    patterns = [item for item in os.listdir() if "pattern" in item and item.endswith(".png")]
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
                print("pattern found at threshold:", chr(int(threshold*100)))
                break

        whiteLevel = 150
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
            if "front" in file or "-f" in args:
                #ellipse size
                ax1, ax2 = 80, 50

                #right ellipse
                cx, cy = 670, 425
                angle = 80
                center = (cx, cy)
                axes = (ax1, ax2)
                cv2.ellipse(img_gray, center, axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)     #last part is important in bitwise function
                cv2.ellipse(mask, center, axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                rightMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]

                #center ellipse
                cx, cy = 515, 465
                angle = 75
                center = (cx, cy)
                axes = (ax1, ax2)
                cv2.ellipse(img_gray, center, axes, angle, 0 , 360, (255,255,255), 1)  #last arg -1 -> full
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)     #last part is important in bitwise function
                cv2.ellipse(mask, center, axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                centerMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                centerWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]


                #left ellipse
                cx, cy = 365, 525
                angle = 68
                center = (cx, cy)
                axes = (ax1, ax2)
                cv2.ellipse(img_gray, center, axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)     #last part is important in bitwise function
                cv2.ellipse(mask, center, axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                leftMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]


                print("mean values(left,center,right):", int(round(leftMean)), int(round(centerMean)), int(round(rightMean)))
                #print("white pixels number(left,center,right):", leftWhiteNumber, centerWhiteNumber, rightWhiteNumber)
            else:
                #ellipse size
                ax1, ax2 = 85, 55

                #left ellipse
                cx, cy = 485, 420
                angle = 95
                center = (cx, cy)
                axes = (ax1, ax2)
                cv2.ellipse(img_gray, center, axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)     #last part is important in bitwise function
                cv2.ellipse(mask, center, axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                leftMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]

                #right ellipse
                cx, cy = 645, 450
                angle = 105
                center = (cx, cy)
                axes = (ax1, ax2)
                cv2.ellipse(img_gray, center, axes, angle, 0 , 360, (255,255,255), 1)
                #masked image
                mask = np.zeros(imgShape, dtype=np.uint8)     #last part is important in bitwise function
                cv2.ellipse(mask, center, axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_gray, img_gray, mask=mask)
                rightMean = maskedImg[np.where(maskedImg>0)].mean()   #by myself :)
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]

                print("mean values(left,right):", int(round(leftMean)), int(round(rightMean)))
                #print("white pixels number(left,right):", leftWhiteNumber, rightWhiteNumber)
            break

        #find resistor
        if "front" in file or "-f" in args:
            resistor = "resistor.png"
            resistorTemp = cv2.imread(resistor, 0)
            w, h = resistorTemp.shape[::-1]
            res = cv2.matchTemplate(img_gray, resistorTemp, cv2.TM_CCOEFF_NORMED)
            threshold = 0.6
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
                print("Resistor:True")
                break
            else:
                print("Resistor:False")

        if "-p" in args:
            cv2.imshow('Detected',img_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


#dorzucić wykrywanie zwarć, tj obszarów pomiędzy lutami
