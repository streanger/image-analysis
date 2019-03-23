import sys
import os

import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, img):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    script_path()
    thugFile = "thug.png"
    thugImage = cv2.imread(thugFile, cv2.IMREAD_UNCHANGED)
    thugImage = thugImage[160:250, 50:350]
    # thugImage = cv2.imread(thugFile, 1)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    
    
    # this position should be changed
    cy = 100
    cx = 100
    
    
    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        img = np.flip(img, 1)
        
        # ********************** enlarge frame **********************
        size = 2
        img = np.repeat(np.repeat(img, size, axis=0), size, axis=1)
        # b_channel, g_channel, r_channel = cv2.split(out)
        # out = cv2.merge((g_channel, r_channel, b_channel))
        (h, w) = img.shape[:2]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        

        
        # '''
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces = face_cascade.detectMultiScale(gray, 2, 2)

        for (x,y,w,h) in faces:
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,50,50), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray, 3, 5)
            if not type(eyes) is tuple:
                eyes = eyes[eyes[:,0].argsort()]
            # print(eyes)
            # print('----'*8)
            for key, (ex,ey,ew,eh) in enumerate(eyes):
                if not key:
                    if len(eyes) == 2:
                        cx = ex + x - 40
                        cy = ey + y
                # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(50,255,50), 2)
        # '''
        
        
        # print(cx, cy)
        
        y_size, x_size, _ = thugImage.shape
        b, g, r, a = cv2.split(thugImage)
        thugColor = cv2.merge((b, g, r))
        roi = img[cy: y_size+cy, cx:x_size+cx]
        mask = a
        mask_inv = cv2.bitwise_not(mask)
        # glasses = cv2.bitwise_and(thugColor, thugColor, mask=mask)
        
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
        img2_fg = cv2.bitwise_and(thugColor, thugColor, mask = mask)
        dst = cv2.add(img1_bg, img2_fg)
        img[cy: y_size+cy, cx:x_size+cx] = dst
        
        
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    
'''
todo:
    -clean up
    -make function to simple extract black object from png
    -make function to simple paste this object in image in any place we want
    -after that add rotation to glasses(object) and resizing as well
    -
    
cascade classifiers:
    https://github.com/opencv/opencv/tree/master/data/haarcascades
'''
