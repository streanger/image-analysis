import sys
import os
import cv2


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def show_image(title, image):
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
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    # cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def mask_image(img, mask, inverted=False):
    if inverted:
        mask = cv2.bitwise_not(mask)
    ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY);
    out = cv2.bitwise_and(img, img, mask=thresh)
    return out
    
    
if __name__ == "__main__":
    script_path()
    files = ['butterfly.jpg', 'parrots.jpg']
    maskFile = 'mask.png'
    for file in files:
        img = cv2.imread(file, 1)
        mask = cv2.imread(maskFile, 0)
        out = mask_image(img, mask, inverted=False)
        show_image('out', out)
        out = mask_image(img, mask, inverted=True)
        show_image('out', out)
