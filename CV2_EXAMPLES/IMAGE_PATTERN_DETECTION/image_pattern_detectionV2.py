#!/usr/bin/python3
import numpy as np
import cv2
import os
import sys
import matplotlib.pyplot as plt

def script_path(subpath=""):
    if subpath:
        path = os.path.realpath(os.path.dirname(subpath))
    else:
        path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def save_file(file, image):
    imgDir = "analysed"
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    path = os.path.join(imgDir, file)
    cv2.imwrite(path, image)

def list_image_files():
    path = script_path()
    fileTypes = (".png", ".jpeg", ".jpg")
    files = [item for item in os.listdir(path) if item.lower().endswith(fileTypes)]
    files = [item for item in files if not "pattern" in item]
    return files

def make_hist(img, cx, cy):
    crop_img = img[cy-2:cy+2, cx-70:cx+70]
    cv2.imshow("crop_img", crop_img)
    hist = plt.hist(crop_img.ravel(),256,[2,254])
    plt.show()
    return True

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
    print(h)
    return [mean(someArray[i:i+h]) for i in range(0,len(someArray),h)]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        files = [args[0]]
        if not os.path.exists(files[0]):
            print("no such file:", files[0])
            sys.exit()
    else:
        files = list_image_files()
        args = ["-f", "-p"]     #set args for all files
        #print(files)
    path = script_path()
    for file in files:
        print("\n" + "-"*30)
        if "front" in file or "-f" in args:
            patterns = ("pattern_front1.png", "pattern_front2.png")
        else:
            patterns = ("pattern_back1.png", "pattern_back2.png")
        img = cv2.imread(file)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_clear = img_gray*1
        imgShape = img.shape[:2]

        for pattern in patterns:
            patternFound = ""
            template = cv2.imread(pattern, 0)
            if not template:
                print("no pattern to search for:", pattern)
                sys.exit()
            w, h = template.shape[::-1]
            loc = []

            #decrease threshold to find pattern matching
            for x in range(60, 80)[::-1]:
                threshold = x/100
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                try:
                    loc.count(0)
                    pass
                except:
                    patternFound = pattern
                    #print("pattern found at threshold:", chr(int(threshold*100)))
                    break
            if patternFound:
                if "-f" in args:
                    if patternFound == "pattern_front1.png":
                        positionCorrect = (0, 0)
                    elif patternFound == "pattern_front2.png":
                        positionCorrect = (-410, +0)    #different
                elif "-b" in args:
                    if patternFound == "pattern_back1.png":
                        positionCorrect = (0, 0)
                    elif patternFound == "pattern_back2.png":
                        positionCorrect = (-825, -235)    #difference between both patterns
                break

        #whiteLevel = 160
        whiteLevel = 150
        #ellipse size
        ax1, ax2 = 70, 30
        axes = (ax1, ax2)
        percentVals = []
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
            if "front" in file or "-f" in args:
                pt = (pt[0] + positionCorrect[0], pt[1] + positionCorrect[1])     #position correct
                #right ellipse
                #cx, cy = pt[0] + 305, pt[1] + 415
                cx, cy = pt[0] + 320, pt[1] + 410   #slim
                angle = 85
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_clear, img_gray, mask=mask)
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                allPixels = mask[np.where(maskedImg>0)].shape[0]
                rightPercentVal = (round(rightWhiteNumber/allPixels*100), (cx-40, cy-90))

                #center ellipse
                cx, cy = pt[0] + 165, pt[1] + 455   #slim
                angle = 78
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)  #last arg -1 -> full
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_clear, img_gray, mask=mask)
                centerWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                allPixels = mask[np.where(maskedImg>0)].shape[0]
                centerPercentVal = (round(centerWhiteNumber/allPixels*100), (cx-40, cy-90))

                #left ellipse
                cx, cy = pt[0] + 20, pt[1] + 510     #slim
                angle = 70
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_clear, img_gray, mask=mask)
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                allPixels = mask[np.where(maskedImg>0)].shape[0]
                leftPercentVal = (round(leftWhiteNumber/allPixels*100), (cx-40, cy-90))

                print("white pixels number(left,center,right): {0}%, {1}%, {2}%".format(round(leftWhiteNumber/allPixels*100), round(centerWhiteNumber/allPixels*100), round(rightWhiteNumber/allPixels*100)))
            else:
                pt = (pt[0] + positionCorrect[0], pt[1] + positionCorrect[1])     #position correct

                #left ellipse
                cx, cy = pt[0] + 146, pt[1] + 402   #slim
                angle = 100
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1)
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_clear, img_gray, mask=mask)
                leftWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                allPixels = mask[np.where(maskedImg>0)].shape[0]
                leftPercentVal = (round(leftWhiteNumber/allPixels*100), (cx-40, cy-90))

                #right ellipse
                cx, cy = pt[0] - 150 + 456, pt[1] + 135 + 282   #slim
                angle = 100
                cv2.ellipse(img_gray, (cx, cy), axes, angle, 0 , 360, (255,255,255), 1) 
                mask = np.zeros(imgShape, dtype=np.uint8)
                cv2.ellipse(mask, (cx, cy), axes, angle, 0 , 360, 255, -1)
                ret, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
                maskedImg = cv2.bitwise_and(img_clear, img_gray, mask=mask)
                rightWhiteNumber = maskedImg[np.where(maskedImg>whiteLevel)].shape[0]
                allPixels = mask[np.where(maskedImg>0)].shape[0]
                rightPercentVal = (round(rightWhiteNumber/allPixels*100), (cx-40, cy-90))

                print("white pixels number(left,right): {0}%, {1}%".format(round(leftWhiteNumber/allPixels*100), round(rightWhiteNumber/allPixels*100)))
            break
        else:
            print("no pattern found in file: {0}".format(file))
            continue

        if "-p" in args:
            COLOR = True
            if COLOR:
                colorImg = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
                toSave = False
                for item in percentVals:
                    if item[0] < 16:            #threshold for red/green
                        toSave = True
                        labelColor = (50, 50, 205)
                    else:
                        labelColor = (50, 205, 50)
                    cv2.putText(colorImg, "{0}%".format(item[0]), item[1], cv2.FONT_HERSHEY_SIMPLEX, 1.1, labelColor, 1, cv2.LINE_AA)
                if toSave:
                    save_file(file, colorImg)     #save modified image

                #cv2.imshow('Detected',colorImg)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
            else:
                cv2.imshow('Detected',img_gray)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
