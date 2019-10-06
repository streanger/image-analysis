import sys
import os
import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
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
    
    
def create_image(h, w, layers=3):
    img = np.zeros((h, w, layers), dtype=np.uint8)
    return img
    
    
def move_stripes(img, size_y, size_x, cut_out):
    if not size_y:
        return img
        
    if not size_x:
        return img
        
    img_size_y, img_size_x = img.shape[:2]
    
    # move all RGB at once
    out = create_image(img_size_y, img_size_x + size_x)      # make bigger image
    STRIPES_NUMBER = img_size_y//size_y + 1
    for stripe in range(STRIPES_NUMBER):
        if stripe%2:
            out[stripe*size_y:(stripe+1)*size_y,:-size_x] = img[stripe*size_y:(stripe+1)*size_y,:]
        else:
            out[stripe*size_y:(stripe+1)*size_y, size_x:] = img[stripe*size_y:(stripe+1)*size_y,:]
            
    if cut_out:
        out = out[:, size_x:-size_x]
    return out
    
    
def example(vertical=True):
    script_path()
    file = 'image01.jpg'
    img = cv2.imread(file, 1)
    for x in range(0, 100, 4):
        if vertical:
            out = move_stripes(img, x, 10, False)
        else:
            out = move_stripes(img, 30, x, False)
        # filename = ('_out_{}.'.format(x)).join(file.split('.'))
        # cv2.imwrite(filename, out)
        show_image('out', out)
    return True
    
    
if __name__ == "__main__":
    script_path()
    file = 'image01.jpg'
    img = cv2.imread(file, 1)
    
    
    # move all RGB at once
    out = move_stripes(img, 30, 10, False)
    show_image('out', out)
    
    
    # move single layer(s)
    # todo
    