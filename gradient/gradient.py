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
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def gradient_image(height, width, start_color, stop_color, direction):
    '''
    parameters:
        height      - image height
        width       - image width
        start_color - RGB (0-255) tuple (R, G, B)
        stop_color  - RGB (0-255) tuple (R, G, B)
        direction   - up/down/right/left supported
        
    not used:
        make horizontal or vertical line and use np.repeat
        out = np.repeat(np.repeat(frame, size, axis=0), size, axis=1)
    '''
    
    r_start, g_start, b_start = start_color
    r_stop, g_stop, b_stop = stop_color
    layers = 3
    # img = np.zeros((h, w), dtype=np.uint8)        # without_layers
    img = np.zeros((height, width, layers), dtype=np.uint8)
    
    if direction in ('up', 'down'):
        # make vertical line(s)
        for x in range(height):
            r_value = r_start + round((r_stop - r_start) * ((x+1)/height))
            g_value = g_start + round((g_stop - g_start) * ((x+1)/height))
            b_value = b_start + round((b_stop - b_start) * ((x+1)/height))
            # print((b_value, g_value, r_value))
            img[x, :] = (b_value, g_value, r_value)
            
    elif direction in ('left', 'right'):
        # make horizontal line(s)
        for x in range(width):
            r_value = r_start + round((r_stop - r_start) * ((x+1)/width))
            g_value = g_start + round((g_stop - g_start) * ((x+1)/width))
            b_value = b_start + round((b_stop - b_start) * ((x+1)/width))
            # print((b_value, g_value, r_value))
            img[:, x] = (b_value, g_value, r_value)
            
    else:
        return False
        
    if direction == 'up':
        img = img[::-1, :]
        
    if direction == 'left':
        img = img[:, ::-1]
        
    return img
    
    
def paste_image(smaller, bigger, x_pos, y_pos):
    ''' paste some image with alpha channel, to another one '''
    
    # ************** handle position and size errors **************
    max_size_y , max_size_x = bigger.shape[:2]
    small_size_y, small_size_x = smaller.shape[:2]
    cut_x, cut_y = 0, 0
    if x_pos + small_size_x > max_size_x:
        cut_x = max_size_x - x_pos
        if cut_x < 1:
            return bigger
        smaller = smaller[:, 0:cut_x]
    if y_pos + small_size_y > max_size_y:
        cut_y = max_size_y - y_pos
        if cut_y < 1:
            return bigger
        smaller = smaller[0:cut_y, :]
    # print("cut_x: {:0=3d}, cut_y: {:0=3d}".format(cut_x, cut_y), end='\r', flush=True)
    
    
    # ************** paste smaller image into bigger, with including alpha channel **************
    B, G, R, alpha = cv2.split(smaller)
    smallerRGB = cv2.merge((B, G, R))
    mask_inv = cv2.bitwise_not(alpha)
    height, width = smallerRGB.shape[:2]
    
    roi = bigger[y_pos:y_pos+height, x_pos:x_pos+width]
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img2_fg = cv2.bitwise_and(smallerRGB, smallerRGB, mask=alpha)
    
    dst = cv2.add(img1_bg, img2_fg)
    out = bigger.copy()         # we shouldn't change original image
    out[y_pos:y_pos+height, x_pos:x_pos+width] = dst
    return out
    
    
if __name__ == "__main__":
    script_path()
    quote = 'example text'
    
    # ******** parameters setup ********
    direction = 'down'
    
    
    # ******** create gradient image ********
    img = gradient_image(200, 1266, (10, 10, 50), (100, 100, 150), direction)
    
    
    # ******** draw quote ********
    cv2.putText(img, quote, (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    
    # ******** paste some image(s) ********
    # smaller = cv2.imread('pigeon.png', cv2.IMREAD_UNCHANGED)
    # heightMain, widthMain = 1200, 900
    # bigger = create_image(heightMain, widthMain)
    # out = paste_image(smaller, bigger, 580, 600)
    # show_image('out', out)    
    
    
    # ******** show image ********
    # show_image('img', img)
    
    
    # ******** save image********
    filename = 'quote_gradient_{}.png'.format(direction)    # convert parameters to filename
    cv2.imwrite(filename, img)
    
    
'''
todo:
    -convert parameters to filename
    -draw quote on image
    -paste some alpha images on main image
    
'''
