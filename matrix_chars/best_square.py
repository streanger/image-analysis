from math import *
from functools import reduce
import itertools
import sys
import os
import numpy as np
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
    
    
def factor_distributions(x):
    '''todo --> check if this function is fully correct'''
    if x <= 0:
        return 0
    i = 2
    e = floor(sqrt(x))
    r = [] #używana jest tablica (lista), nie bepośrednie wypisywanie
    while i <= e:
        if x % i == 0:
            r.append(i)
            x /= i
            e = floor(sqrt(x))
        else:
            i += 1
    if x > 1:
        r.append(x)
        r.append(1)
    return [int(item) for item in r]
    


def variations(data):
    '''https://stackoverflow.com/questions/40709488/all-possibilities-to-split-a-list-into-two-lists'''
    pairs = []
    dataLen = len(data)
    for pattern in itertools.product([True, False], repeat=dataLen):
        some = [int(x[1]) for x in zip(pattern, data) if x[0]]
        thing = [int(x[1]) for x in zip(pattern, data) if not x[0]]
        pair = [some, thing]
        if not all(pair):
            continue
        pairs.append(pair)

    # some way, to remove duplicates
    # https://stackoverflow.com/questions/2213923/removing-duplicates-from-a-list-of-lists
    sortedPairs = [sorted(pair) for pair in pairs]
    pairs = list(out for out, _ in itertools.groupby(sortedPairs))
    return pairs
    
    
def flatten(data):
    return [x for y in data for x in y]
    
    
def best_square(dim_x, dim_y, reverse=False):
    '''generate variations
       e.g. rectange 2 x 15 --> 5 x 6
    '''
    full = dim_x * dim_y
    data = factor_distributions(full)
    pairs = variations(data)
    
    # a, b stored
    # sides = [(a, b, abs(reduce((lambda x, y: x * y), a) - reduce((lambda x, y: x * y), b))) for a, b in pairs]
    
    # a, b multiplied
    sides = [(reduce((lambda x, y: x * y), a), reduce((lambda x, y: x * y), b)) for a, b in pairs]
    sides = [(a, b, abs(a - b)) for a, b in sides]
    sortedSides = sorted(sides, key=lambda x: x[2], reverse=reverse)
    best = list(out for out, _ in itertools.groupby(sortedSides))
    return best[0][:2]
    
    
def create_image(w, h):
    img = np.zeros((w, h, 3), dtype=np.uint8)
    return img
    
    
def rect_to_square_example():
    img = create_image(450, 700)
    a, b = 248, 60
    x, y = best_square(a, b)
    print('best square from ({}, {}) is: ({}, {})'.format(a, b, x, y))
    
    # draw rectange
    startRect = 20
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'rectangle', (10, 75), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.putText(img, 'a : {}'.format(a), (10, 150), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.putText(img, 'b : {}'.format(b), (10, 225), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.rectangle(img, (startRect, startRect*15), (startRect + a, startRect*15 + b), (50, 255, 50), 1)
   
    
    # draw square
    startRect = 20
    cv2.putText(img, 'square', (410, 75), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.putText(img, 'x : {}'.format(x), (410, 150), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.putText(img, 'y : {}'.format(y), (410, 225), font, 2, (155, 155, 155), 2, cv2.LINE_AA)
    cv2.rectangle(img, (startRect + 400, startRect*15), (startRect + 400 + x, startRect*15 + y), (50, 255, 50), 1)
    
    cv2.imwrite('example.png', img)
    show_image('img', img)
    return True
    
    
def best_square_two(dim_x, dim_y, reverse=False):
    center = (dim_x * dim_y)**(0.5)
    '''
    e.g. 22540**(0.5) --> 150.13....
    x, y = 150, 151
    calc result -> if == dim_x * dim_y => OK
    else -> x, y = 149, 152
    ...
    if worst case:
        x, y = 1, dim_x * dim_y
        
    it seems to be much simple than my previous solution(which let me to learn a lot)
    '''
    return (1, 2)
    
    
if __name__ == "__main__":
    script_path()
    
    a, b = 248, 60
    x, y = best_square(a, b)
    print('best square from ({}, {}) is: ({}, {})'.format(a, b, x, y))
    
    
    # rect_to_square_example()
    
    
'''
INFO:
    https://pl.wikipedia.org/wiki/Wariacja_z_powtórzeniami
    https://pl.wikipedia.org/wiki/Wariacja_bez_powtórzeń
    
'''
