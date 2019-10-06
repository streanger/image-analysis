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
    
    
def roll_image(img, x_axis, y_axis):
    img = np.roll(img, y_axis, axis=0)   # axis: 0-up-down, 1-right-left
    img = np.roll(img, x_axis, axis=1)   # axis: 0-up-down, 1-right-left
    return img
    
    
def create_image(h, w, layers=3, without_layers=False):
    if without_layers:
        img = np.zeros((h, w), dtype=np.uint8)
    else:
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
            out[stripe*size_y:(stripe+1)*size_y, :-size_x] = img[stripe*size_y:(stripe+1)*size_y,:]
        else:
            out[stripe*size_y:(stripe+1)*size_y, size_x:] = img[stripe*size_y:(stripe+1)*size_y,:]
            
    if cut_out:
        out = out[:, size_x:-size_x]
    return out
    
    
def move_layers(img, strike, order_position='BGR', order_up_down='BGR'):
    '''
        order_position  --from left to right-left
        order_up_down   --the way in which layers lay on each other
    '''
    
    img_size_y, img_size_x = img.shape[:2]
    b_channel, g_channel, r_channel = cv2.split(img)
    layers = {
        'B': b_channel,
        'G': g_channel,
        'R': r_channel
        }
        
    stripe_left = create_image(img_size_y, img_size_x + strike*2, without_layers=True)
    stripe_center = create_image(img_size_y, img_size_x + strike*2, without_layers=True)
    stripe_right = create_image(img_size_y, img_size_x + strike*2, without_layers=True)
    
    stripe_left[:, :(-2*strike)] = layers[order_position[0]]
    stripe_center[:, strike:-strike] = layers[order_position[1]]
    stripe_right[:, 2*strike:] = layers[order_position[2]]
    
    stripes = {
        order_position[0] : stripe_left,
        order_position[1] : stripe_center,
        order_position[2] : stripe_right
        }
        
    stripe = cv2.merge((stripes[order_up_down[0]],
                        stripes[order_up_down[1]],
                        stripes[order_up_down[2]]))
    return stripe
    
    
def move_stripes_many(img, size_y, size_x, strike=0, order_position='BGR', order_up_down='BGR', vertical=False, cut_out=False):
    if not size_y:
        return img
    if vertical:
        # Rotate an array by 90 degrees in the counter-clockwise direction
        # k: Number of times the array is rotated by 90 degrees.
        img = np.rot90(img, k=1)
        
    resize_x = strike + max(size_x, strike)
    img_size_y, img_size_x = img.shape[:2]
    
    # move all RGB at once
    out = create_image(img_size_y, img_size_x + resize_x)      # make bigger image
    STRIPES_NUMBER = img_size_y//size_y + 1
    for stripe in range(STRIPES_NUMBER):
        part = img[stripe*size_y:(stripe+1)*size_y,:]
        if not part.any():
            continue
        if strike:
            # part_moved = move_layers(part, strike, order_position='BGR', order_up_down='BGR')
            part_moved = move_layers(part, strike, order_position=order_position, order_up_down=order_up_down)
        else:
            part_moved = part
        edge = abs(resize_x - 2*strike)
        
        # it works but its not optimized :(
        if stripe%2:
            if edge:
                out[stripe*size_y:(stripe+1)*size_y, :-edge] = part_moved
            else:
                out[stripe*size_y:(stripe+1)*size_y, :] = part_moved
        else:
            if edge:
                out[stripe*size_y:(stripe+1)*size_y, edge:] = part_moved
            else:
                out[stripe*size_y:(stripe+1)*size_y, :] = part_moved
                
    if vertical:
        out = np.rot90(out, k=3)        # reverse way
        
    if cut_out:
        out = out[:, max(size_x, strike):-max(size_x, strike)]
    return out
    
    
def example(status=True):
    script_path()
    file = 'image01.jpg'
    img = cv2.imread(file, 1)
    for x in range(0, 100, 4):
        if status:
            out = move_stripes(img, x, 10, False)
        else:
            out = move_stripes(img, 30, x, False)
        # filename = ('_out_{}.'.format(x)).join(file.split('.'))
        # cv2.imwrite(filename, out)
        show_image('out', out)
    return True
    
    
def example_many(status=True):
    script_path()
    file = 'image01.jpg'
    img = cv2.imread(file, 1)
    for x in range(0, 50, 4):
        if status:
            out = move_stripes_many(img, 30, 10, strike=x, strike_order='BGR', vertical=False, cut_out=True)
        else:
            out = move_stripes_many(img, 30, x, strike=6, strike_order='BGR', vertical=False, cut_out=True)
        filename = ('_out_many_{}.'.format(x)).join(file.split('.'))
        cv2.imwrite(filename, out)
        show_image('out', out)
        
    for item in ['BGR', 'GRB', 'BRG']:
        out = move_stripes_many(img, 30, 10, strike=15, order_position=item, order_up_down='RGG', vertical=False, cut_out=False)
        show_image('out', out)
    return True
    
    
if __name__ == "__main__":
    script_path()
    file = 'image01.jpg'
    # file = 'image02.jpg'
    img = cv2.imread(file, 1)
    
    
    # move all RGB at once
    out = move_stripes(img, 30, 10, False)
    show_image('out', out)
    
    
    # move single layer(s)
    out = move_stripes_many(img, 30, 10, strike=5, order_position='BGR', order_up_down='BGR', vertical=False, cut_out=False)
    show_image('out', out)
    
    
    # example(status=True)
    # example_many(status=True)
    
    
'''
todo:
    -swap single layers(s)                                          (+)
    -strike value (R -<value>- G -<value>- B)                       (+)
    -choose positions ->: RGB, BGR, ...                             (+)
    -choose vertical-horizontal (make transpose and then reverse)   (+)
'''
