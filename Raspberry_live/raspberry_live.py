import os
import sys
import numpy as np
import cv2


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

    
def main(args):
    some = 0
    other = 0
    multi = 5
    while(True):
        cap = cv2.VideoCapture(0)
        if (not cap.isOpened()):
            return False
    
        ret, frame = cap.read()         # Capture frame-by-frame

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB) # is the correct syntax.
        gray = backtorgb
        
        
        # ********************** enlarge frame **********************
        size = 2
        gray = np.repeat(np.repeat(gray, size, axis=0), size, axis=1)
        
        
        # ********************** draw contours **********************
        out = draw_over(gray)
        
        
        # Display the resulting frame
        cv2.imshow('frame', out)
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
    -
    
'''
