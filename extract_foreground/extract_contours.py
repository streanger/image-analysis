'''
this is very copied script
https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
'''

import os
import sys
import cv2


def script_path():
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current)
    return current

    
if __name__ == "__main__":
    script_path()
    
    #reading the image 
    # file = 'test.png'
    # file = 'many.jpg'
    # file = 'DSC_9686__35305.1486048373.960.550.jpg'
    # file = 'img1_initial.jpg'
    file = 'very_test.png'
    
    
    if True:
        image = cv2.imread(file)
        # edged = cv2.Canny(image, 10, 250)
        edged = cv2.Canny(image, 1, 250)
        cv2.imshow("Edges", edged)
        cv2.waitKey(0)
        
        # applying closing function 
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("Closed", closed)
        # cv2.waitKey(0)
         
        # finding_contours 
        im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        cv2.imshow("Output", image)
        cv2.waitKey(0)
    
    
    if False:
        image = cv2.imread(file)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(image, 10, 250)
        # (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        im2, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            if w>50 and h>50:
                idx+=1
                new_img=image[y:y+h,x:x+w]
                cv2.imwrite(str(idx) + '.png', new_img)
        cv2.imshow("im",image)
        cv2.waitKey(0)


