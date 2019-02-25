import os
import sys
import time
import numpy as np
import cv2

import image_rgb_roll

def script_path():
    '''set current path to script_path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path

def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
def resize_image(img, newSize):
    height = round((img.shape[0])*(newSize/100))
    width = round((img.shape[1])*(newSize/100))
    resized = cv2.resize(img, (width, height))
    return resized
    
    
def draw_over(img):
    # add something
    out = img.copy()
    cv2.rectangle(out,(384, 0),(510, 128),(155, 255, 155), 2)
    return out
    
    
def draw_contours(image):
    ''' find contours and draw over '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)           # 30 is ok
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # sort contours
    contoursSorted = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    loopRange = 50
    if len(contoursSorted) < 50:
        loopRange = len(contoursSorted)
    if not len(contoursSorted):
        raise ValueError('A very specific bad thing happened.')
    print(len(contoursSorted))
    for key, contour in enumerate(contoursSorted[:loopRange]):
        # color_contours = (150, 255, 150)            # green - color for contours
        color_contours = (50, 255, 50)            # green - color for contours
        cv2.drawContours(image, contoursSorted, key, color_contours, 1, 4, hierarchy)
    return image
    
    
def main(args):
    cap = cv2.VideoCapture(0)
    print("press 'q' to exit...")
    
    while(True):
        # if (not cap.isOpened()):
            # return False
            
        ret, frame = cap.read()         # Capture frame-by-frame
        if not ret:
            continue
        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB) # is the correct syntax.
        
        # ********************** enlarge frame **********************
        size = 1
        out = np.repeat(np.repeat(frame, size, axis=0), size, axis=1)
        b_channel, g_channel, r_channel = cv2.split(out)
        out = cv2.merge((g_channel, r_channel, b_channel))
        
        
        # ********************** roll image **********************
        # seconds = int(time.strftime("%S"))
        # now = round(time.time()%1*1000)/200
        # out = image_rgb_roll.rgb_roll(out, now, 10)
        # out = image_rgb_roll.rgb_roll(out, now, now)
        out = image_rgb_roll.rgb_roll(out, 45, 3)
        
        
        # ********************** draw contours **********************
        try:
            # pass
            out = draw_contours(out)
        except:
            print("fail to draw conturs")
            # thats why we need to extract contours first and check if they exist -> this is very todo
            continue
        
        # Display the resulting frame
        cv2.imshow('out', out)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # '''
    return True
    
    
if __name__ == "__main__":
    current_path = script_path()
    main(sys.argv[1:])
    
    
'''
todo:
    -add some characters falling down, colored, and chinnese
    -return contours in funtion
    -draw with antother one
    -extract person from image and draw over different background
    -
    
'''
