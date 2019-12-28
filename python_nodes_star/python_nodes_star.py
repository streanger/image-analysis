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
    
    
def draw_star(img, color=(50, 50, 250), random_points=False, full=True, circles=False):
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
    
    
def generate_points(img, move_y, move_x, shuffle_points=False):
    height, width, layers = img.shape
    height -= 1
    width -= 1
    
    # get nine nodes
    points = [(y, x) for x in [0, round(height/2), height] for y in [0, round(width/2), width]]
    points = [(y + move_y, x + move_x) for (y, x) in points]
    
    if shuffle_points:
        shuffle(points)
        
    return points
    
    
def draw_from_points(img, points, color=(50, 50, 250), nodes=True, arrows=True, cover=False, number=8):
    '''
    parameters:
        img     -
        number  - default is 8 (unlock trace)
        color   -
        nodes   -
        arrows  -
        cover   -
        number  -
    '''
    
    out = img.copy()
    
    # pairs are hardcoded here(from previous function)
    pairs = [
        (7, 2),
        (2, 9),
        (9, 4),
        (4, 3),
        (3, 8),
        (8, 1),
        (1, 6),
        (6, 5),
        (5, 7),
        ]
        
    pairs = pairs[:number]
    
    if nodes:
        # draw nodes
        for point in points:
            cv2.circle(out, point, 5, (220, 220, 220), -1) 
            
    for (start_point, stop_point) in pairs:
        # draw lines
        if not arrows:
            cv2.line(out, points[start_point-1], points[stop_point-1], color, 2)
        
        else:
            center_point = (round((points[start_point-1][0] + points[stop_point-1][0])/2),
                            round((points[start_point-1][1] + points[stop_point-1][1])/2))
                            
            arrow_color = tuple(round(item*0.6) for item in color)
            arrow_color_background = tuple(round(item*0.7) for item in color)
            
            
            cv2.arrowedLine(out, points[stop_point-1], center_point, arrow_color_background, 2, tipLength = 0.12)
            cv2.arrowedLine(out, points[stop_point-1], center_point, arrow_color, 2, tipLength = 0.10)
            
            if cover:
                cv2.line(out, points[start_point-1], points[stop_point-1], color, 2)    # cover whole line
            else:
                cv2.line(out, center_point, points[start_point-1], color, 2)
    return out
    
    
if __name__ == "__main__":
    script_path()
    
    if False:
        # single star, previous function
        img = create_image(400, 400)
        img_star = draw_star(img)
        img_start_around = make_around(img_star, 50)
        cv2.imwrite('star.png', img_start_around)
        
        
    if True:
        for x in range(10):
            img = create_image(400, 400)
            move = 50
            points = generate_points(img, move, move, shuffle_points=True)
            # find random points
            
            img_around = make_around(img, move)
            color = (randrange(256), randrange(256), randrange(256))
            out = draw_from_points(img_around, points, color=color, nodes=True, arrows=True, cover=False, number=8)
            cv2.imwrite('trace_{}.png'.format(x), out)
            
            
'''
todo:
    -draw arrow between lines as direction      (+)
    -add circles in nodes                       (+)
    -mark start/stop of the trace               (-)
    -fix points/pairs dependency                (-)
    
'''
