"""
matrix characters rain
modified at 19.06.2022
"""
import sys
import os
import time
import random
import string
import numpy as np
import cv2
# from collections import deque
from PIL import Image, ImageDraw, ImageFont


def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
    
def show_image(title, image):
    """
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    """
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def create_image(h, w, layers=3):
    """create image"""
    img = np.zeros((h, w, layers), dtype=np.uint8)
    return img
    
    
if __name__ == "__main__":
    script_path()
    
    # ******* matrix characters *******
    chinesseChars = 2*'端午节就要到了價价価樂乐楽氣气気廳厅庁發发発勞劳労劍剑剣歲岁歳權权権燒烧焼贊赞賛兩两両譯译訳觀观観營营営處处処齒齿歯驛驿駅櫻樱桜產产産藥药薬讀读読'
    chinesseChars += string.printable
    chinesseCharsList = list(chinesseChars)
    
    # ******* create image *******
    width, height = 1920, 1080
    image = create_image(height, width, 3)
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    
    # ******* window setup *******
    fullscreen = True
    window_title = 'img'
    if fullscreen:
        cv2.namedWindow(window_title, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_title)
        
    # ******* parts setup *******
    parts_limit = 500
    parts = []
    fontpath = "./simsun.ttc" # <== 这里是宋体路径
    small_digit = 20
    big_digit = 25
    font_small = ImageFont.truetype(fontpath, small_digit)
    font_big = ImageFont.truetype(fontpath, big_digit)
    random_y_range = round(height*0.05)
    items_width = [x for x in range(0, width, big_digit*2)]
    items_back_width = [x for x in range(small_digit+1, width, small_digit*3)]
    
    # ******* main loop *******
    while True:
        # ******* create new parts *******
        parts_number = len(parts)
        if parts_number < parts_limit:
            for x in range(10):
                if x%2:
                    # ******* background *******
                    rand_color = random.randrange(-30, 30)
                    b, g, r = 80 + rand_color, 150, 80 + rand_color
                    speed = random.randrange(8, 25)
                    background = True
                    randX = random.choice(items_back_width)
                else:
                    # ******* front *******
                    rand_color = random.randrange(-50, 50)
                    b, g, r = 120 + rand_color, 240, 120 + rand_color
                    speed = random.randrange(3, 20)
                    background = False
                    randX = random.choice(items_width)
                    
                randY = random.randrange(random_y_range)
                character = {
                    'posx': randX,
                    'posy': randY,
                    'char': random.choice(chinesseCharsList),
                    'color': (b, g, r),
                    'speed': speed,
                    'background': background,
                }
                parts.append(character)
                
        # ******* draw & update characters *******
        draw.rectangle((0, 0, width, height), fill=0)  # clear before draw new
        updated = []
        for character in parts:
            character['posy'] += character['speed']
            if character['posy'] > height:
                continue
            if character['background']:
                draw.text((character['posx'], character['posy']), character['char'], font=font_small, fill=character['color'])
            else:
                draw.text((character['posx'], character['posy']), character['char'], font=font_big, fill=character['color'])
            updated.append(character)
        parts = updated
        
        # ******* show created image *******
        img = np.array(img_pil)  # PIL -> cv2 image
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
            
    # ******* cleanup *******
    cv2.destroyAllWindows()
    
"""
19.06.2022
    -use deque if want to insertleft background character(s)
    -variable digit size depend on background flag?
    -think of better handling of characters update, creation and deletion
"""
