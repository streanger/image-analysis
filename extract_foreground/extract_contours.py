'''
this is very copied script
https://www.quora.com/How-can-I-detect-an-object-from-static-image-and-crop-it-from-the-image-using-openCV
'''

import os
import sys
import cv2
import numpy as np


def script_path():
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current)
    return current
    
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
def make_dir(new_dir):
    '''make new dir, switch to it and retur new path'''
    current = os.path.realpath(os.path.dirname(sys.argv[0]))
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(current, new_dir)
    return new_path
    
    
def create_blank_image(height, width):
    image = np.zeros((height, width, 1), np.uint8)
    return image
    
    
def extract_contours(image, bound=False):
    # edged = cv2.Canny(image, 10, 250)
    edged = cv2.Canny(image, 10, 250)
    # edged = cv2.Canny(image, x, 250)
    edgedThree = cv2.merge((edged, edged, edged))
    # cv2.imshow("Edges", edged)
    # cv2.waitKey(0)
    
    # applying closing function 
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, x))      # 3 - 5 is ok
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))      # 3 - 5 is ok
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
     
    # finding_contours 
    im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height, width = image.shape[:2]
    mask = create_blank_image(height, width)
    contours = sorted(cnts, key=len, reverse=True)
    
    
    for c in cnts:
        peri = cv2.arcLength(c, True)
        # approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        approx = cv2.approxPolyDP(c, 0.0001 * peri, True)
        cv2.drawContours(mask, [approx], -1, (255, 255, 255), -1)
    
    
    # just to show edges and masked on the same image
    if False:
        catImages = np.concatenate((edgedThree, image), axis=1)
        # cv2.putText(catImages, "{}".format(x), (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 255)
        # cv2.imshow("catImages", catImages)
        cv2.imshow("Output", image)
        cv2.waitKey(0)
        
    out = cv2.bitwise_or(image, image, mask=mask)
    B, G, R = cv2.split(out)
    out = cv2.merge((B, G, R, mask))
    
    # cut to contours
    # if contours:
    if bound:
        x, y, w, h = cv2.boundingRect(contours[0])
        out = out[y:y+h, x:x+w]
    return out
    
    
if __name__ == "__main__":
    script_path()
    
    #reading the image 
    # file = 'test.png'
    file = 'many.jpg'
    file = 'flower.jpg'
    # file = 'DSC_9686__35305.1486048373.960.550.jpg'
    # file = 'img1_initial.jpg'
    # file = 'very_test.png'
    
    new = make_dir('extracted')
    files = [item for item in os.listdir() if item.endswith(('.png', '.jpg'))]
    # files = [file]
    for file in files:
        # for x in range(1, 255):
        img = cv2.imread(file)
        out = extract_contours(img)
        # show_image('out', out)
        filename = os.path.join(new, '_extracted.'.join(file.split('.')))
        print(filename)
        cv2.imwrite(filename, out)
        
        
        '''
        if True:
            image = cv2.imread(file)
            edged = cv2.Canny(image, 10, 250)
            # edged = cv2.Canny(image, x, 250)
            edgedThree = cv2.merge((edged, edged, edged))
            # cv2.imshow("Edges", edged)
            # cv2.waitKey(0)
            
            # applying closing function 
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (x, x))      # 3 - 5 is ok
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))      # 3 - 5 is ok
            closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
            # cv2.imshow("Closed", closed)
            # cv2.waitKey(0)
             
            # finding_contours 
            im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for c in cnts:
                peri = cv2.arcLength(c, True)
                # approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                approx = cv2.approxPolyDP(c, 0.0001 * peri, True)
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 1)
            
            catImages = np.concatenate((edgedThree, image), axis=1)
            # cv2.putText(catImages, "{}".format(x), (250, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 255)
            # cv2.imshow("catImages", catImages)
            cv2.imshow("Output", image)
            cv2.waitKey(0)
        '''
        
        
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
        
        