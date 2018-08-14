#!/usr/bin/python3
#updated version of resizeImageV2.py
import sys
import os
import cv2

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

def get_files(fileTypes=("png", "jpeg", "jpg")):
    files = [item for item in os.listdir() if (item.lower()).split('.')[-1] in fileTypes]
    return files

def resize_image(fileName, newSize=100):
    subDir = "RESIZED"
    image = cv2.imread(fileName)
    height = round((image.shape[0])*(newSize/100))
    width = round((image.shape[1])*(newSize/100))
    resized = cv2.resize(image, (width, height))

    path = os.path.join(os.getcwd(), subDir)
    path = os.path.join(path, fileName)
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    cv2.imwrite(path, resized)
    return True

if __name__ == "__main__":
    path = script_path()
    files = get_files()
    for file in files:
        resize_image(file, 50)
    print("finished...")
