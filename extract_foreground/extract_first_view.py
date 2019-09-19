import os
import sys
import time
from statistics import mean
import numpy as np
import cv2


def script_path():
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current)
    return current
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
def create_blank_image(height, width):
    # image = np.zeros((height, width, 3), np.uint8)
    image = np.zeros((height, width, 1), np.uint8)
    # image += 55
    return image
    
    
def make_dir(new_dir):
    '''make new dir, switch to it and retur new path'''
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(current, new_dir)
    return new_path
    
    
def extract_image(img, toErode, valueX, valueY):
    '''it will extract image in the simplest case'''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = img.shape[:2]
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53, 4)     # 53, 5 OK
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53, value)     # 53, 5 OK
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, valueX, valueY)     # 53, 5 OK
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53, 11)     # 53, 5 OK
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)     # 53, 5 OK
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=len, reverse=True)
    # contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]                              # get largest five contour area
    
    mask = create_blank_image(height, width)
    cnt = contours[:1]
    x, y, w, h = cv2.boundingRect(cnt[0])
    cv2.drawContours(mask, cnt, -1, (255, 255, 255), -1)        
    out = cv2.bitwise_or(img, img, mask=mask)
    B, G, R = cv2.split(out)
    out = cv2.merge((B, G, R, mask))
    if toErode:
        kernel = np.ones((3, 3), np.uint8)
        out = cv2.erode(out, kernel, iterations=1)
        
    out = out[y:y+h, x:x+w]         # bound rect
    return out
    
    
if __name__ == "__main__":
    script_path()
    # file = 'test.png'
    file = 'very_test.png'
    file = 'flower.jpg'
    # file = 'img1_initial.jpg'
    files = [file]
    # files = [item for item in os.listdir() if item.endswith(('.png', '.jpg'))]
    
    if False:
        for key, file in enumerate(files):
            img = cv2.imread(file, 1)
            for y in range(25):
                out = extract_image(img, True, y)
                show_image('out', out)
            cv2.imwrite('out.png', out)
            
            
    # ********************* test different combinations *********************
    
    new = make_dir(file.split('.')[0])
    img = cv2.imread(file, 1)
    for x in range(60):
        for y in range(20):
            try:
                out = extract_image(img, True, x, y)
                filename = os.path.join(new, '{}_{}.png'.format(x, y))
                # show_image('out', out)
                cv2.imwrite(filename, out)
            except:
                print('fail: {}, {}'.format(x, y))
                
                
                
'''
todo:
    -extract contours
    -make mask
    -cut masked image to contours
    -save with alpha channel
    
    
info:
    https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=boundingrect
    https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
    
    
'''


