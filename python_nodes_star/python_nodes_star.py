import sys
import os
from random import shuffle, randrange
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
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def create_image(height, width, layers=3):
    img = np.zeros((height, width, layers), dtype=np.uint8)
    return img
    
    
def make_around(img, space_size):
    '''space_size -integer; 2 is the lowest value for proper read; try to increase value and look for decoding time'''
    color = 0
    current_h, current_w, layers = img.shape
    new_image = np.ones((current_h+space_size*2, current_w+space_size*2, layers), dtype=np.uint8)*color
    new_image[space_size:-space_size, space_size:-space_size] = img
    return new_image
    
    
def draw_star(img, color=(50, 50, 250), random_points=False, full=True):
    '''with nine nodes'''
    out = img.copy()
    
    height, width, layers = img.shape
    height -= 1
    width -= 1
    
    # get nine nodes
    points = [(x, y) for x in [0, round(height/2), height] for y in [0, round(width/2), width]]
    
    # draw stuff
    # 7 2 9 4 3 8 1 6 7
    pairs = [
        (7, 2),
        (2, 9),
        (9, 4),
        (4, 3),
        (3, 8),
        (8, 1),
        (1, 6),
        (6, 7),
        ]
    if random_points:
        shuffle(points)
        
    if not full:
        pairs = pairs[:-1]
        
    for (start_point, stop_point) in pairs:
        cv2.line(out, points[start_point-1], points[stop_point-1], color, 2)
        
    return out
    
if __name__ == "__main__":
    script_path()
    
    if False:
        img = create_image(400, 400)
        img_star = draw_star(img)
        img_start_around = make_around(img_star, 50)
        cv2.imwrite('star.png', img_start_around)
        
        
    if True:
        for x in range(10):
            img = create_image(400, 400)
            img_star = draw_star(img, color=(randrange(256), randrange(256), randrange(256)), random_points=True, full=False)
            img_start_around = make_around(img_star, 50)
            cv2.imwrite('star_{}.png'.format(x), img_start_around)
            
            
'''
todo:
    -draw arrow between lines as direction
    -
    
'''
