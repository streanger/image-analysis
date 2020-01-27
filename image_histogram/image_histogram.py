'''
date of current version: 27.01.2020
'''
import sys
import os
import math
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pylab import savefig
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
    
    
def create_gradient_image(h, w, value):
    # img = np.array([(x**0.87+x*10 + 20)%256 for x in range(w*h)], dtype=np.uint8)
    # img = np.array([(x**value+x*10 + 20)%256 for x in range(w*h)], dtype=np.uint8)
    # img = np.array([(x**value - x*value*10)%256 for x in range(w*h)], dtype=np.uint8)
    img = np.array([(x)%256 for x in range(w*h)], dtype=np.uint8)
    img = np.resize(img, (h, w))
    return img
    
    
def histogram_data(img):
    '''create histogram data from image'''
    # split into layers
    shape = img.shape
    if len(shape) == 2:
        flatten_image = [x for y in img.tolist() for x in y]
        many_data = [('GRAYSCALE', flatten_image)]
    else:
        names = ['BLUE', 'GREEN', 'RED', 'ALPHA']
        layers = cv2.split(img)
        many_data = [(names[key], [x for y in layer.tolist() for x in y]) for key, layer in enumerate(layers)]
    return many_data
    
    
def draw_hist(many_data, title):
    ''' put list of data to plot, as many_data variable '''
    bins = np.linspace(0, 255, 255)        # last parameter is width of columns
    colors = []
    hist_number = len(many_data)
    probability = False
    for key, (name, data) in enumerate(many_data):
        cmap = plt.get_cmap('jet')  # https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
        current_color = cmap(key/hist_number)
        colors.append(current_color)
        plt.hist(data, bins, alpha=0.5, histtype='bar', ec='black', density=probability, label='this', color=current_color)
        
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if probability:
        plt.ylabel('Probability')
    else:
        plt.ylabel('Elements')
    plt.xlabel('Score')
    
    #create legend
    handles = [Rectangle((0,0), 1, 1, alpha=0.5, color=c, ec="k") for c in colors]
    labels= ["{}: {}".format(key, many_data[key][0]) for key, _ in enumerate(colors)]       # make it more clear
    plt.legend(handles, labels)
    
    plt.suptitle(title)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')       #full window
    
    
    # plt.savefig('some_plt.png')       # think of bigger one
    plt.show()
    plt.close()
    return True
    
    
def draw_bar(list_data, title):
    '''
    info:
        -use "flatten_image" for that
        -example:   
            flatten_image = [x for y in img.tolist() for x in y]
    '''
    # data = Counter(flatten_image)
    data = Counter(list_data)
    data_list = list(data.items())
    sorted_data = sorted(data_list, key=lambda x: x[0])
    labels, values = list(zip(*sorted_data))
    
    # calc to percent
    percent_value = False
    if percent_value:
        values_sum = sum(values)
        values = [round((item/values_sum)*100) for item in values]
        
    # complete missed values in labels - need to be full 0-255
    data_to_draw = [labels, values]
    
    # draw bar
    indexes = np.arange(len(labels))
    width = 1
    
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.suptitle(title)
    plt.show()
    return True
    
    
if __name__ == "__main__":
    script_path()
    file = 'lamps.png'
    
    img = cv2.imread(file, 1)
    show_image('img', img)
    many_data = histogram_data(img)
    draw_hist(many_data, 'IMAGE HISTOGRAM')
