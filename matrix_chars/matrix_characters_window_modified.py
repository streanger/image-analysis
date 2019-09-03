'''this script is for make matrix characters

    THIS SCRIPT SHOULD BE MODIFIED AS IT WAS DESCRIBED IN INFO ON THE BOTTOM
'''
import sys
import os
import time
import random
import string
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from best_square import best_square


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
    
    
def overlay_image(img):
    out = img.copy()
    return out
    
    
def create_image(h, w, layers=3):
    img = np.zeros((h, w, layers), dtype=np.uint8)
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
    
    
def cv2_fonts_example():
    img = create_image(725, 1800)
    img += 33
    fonts = [item for item in dir(cv2) if item.startswith('FONT')]
    for key, font in enumerate(fonts):
        # font = cv2.FONT_HERSHEY_SIMPLEX
        print('{:02}. {}'.format(key, font))
        text = '{:02}. {} -> OpenCV {}'.format(key, font, chr(512))
        cv2.putText(img, text, (20, 75 + key*75), getattr(cv2, font), 2, (255,255,255), 2, cv2.LINE_AA)
    
    cv2.imwrite('cv2_fonts.png', img)
    show_image('some', img)
    return True
    
    
def make_mask(text, file):
    fontpath = "./simsun.ttc" # <== 这里是宋体路径 
    font = ImageFont.truetype(fontpath, 122)
    mask = font.getmask(text)
    a, b = best_square(len(mask), 1)
    img = np.array(mask)
    out = np.reshape(img, (a, b))
    cv2.imwrite(file, out)
    return True
    
    
def create_masks():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)  #it seems to be quite important
    new_dir = 'masked_characters'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        
    for x in range(256):
        try:
            text = chr(x)
            file = os.path.join(currentPath, new_dir, '{}.png'.format(text))
            make_mask(text, file)
        except:
            print('error:', x)
    return True
    
    
def alpha(img):
    B, G, R, alpha = cv2.split(img)
    out = cv2.merge((B, G, R, G))
    return out
    
    
if __name__ == "__main__":
    script_path()
    # img = cv2.imread('view.png', 1)
    # cv2_fonts_example()
    
    
    # **************** IMAGE height-width example ****************
    # width = 1266
    # height = 866
    # img = create_image(height, width, 3)
    # cv2.imwrite('some.png', img)
    # sys.exit()
    
    
    
    # **************** draw chinesse char in PIL & convert image to numpy array ****************
    pos = 0
    
    
    # ************** this is important **************
    # digitSize = 15      # size of single digit
    digitSize = 20      # size of single digit
    
    
    # width, height = 1920, 1080      # full-hd
    width, height = 1366, 768
    
    fixed_height = 20
    line_with_fixed_height = create_image(fixed_height, width, 3)
    
    
    # widthItems = [x for x in range(0, width, 25)]
    widthItems = [x for x in range(0, width, digitSize*2)]
    widthItemsBack = [x for x in range(digitSize + 1, width, digitSize*3)]
    
    chinesseChars = ""
    chinesseChars = 3*'端午节就要到了價价価樂乐楽氣气気廳厅庁發发発勞劳労劍剑剣歲岁歳權权権燒烧焼贊赞賛兩两両譯译訳觀观観營营営處处処齒齿歯驛驿駅櫻樱桜產产産藥药薬讀读読'
    # chinesseChars += string.ascii_lowercase
    chinesseChars += string.printable
    
    
    img = create_image(height, width, 3)
    parts = []
    cv2.namedWindow('img', cv2.WINDOW_GUI_NORMAL)
    while True:
        fontpath = "./simsun.ttc" # <== 这里是宋体路径 
        # font = ImageFont.truetype(fontpath, 122)
        # font = ImageFont.truetype(fontpath, 40)
        font = ImageFont.truetype(fontpath, digitSize)
        
        newParts = []
        
        # do not create new parts if its too much of current ones
        # if len(parts) < 150:
        if len(parts) < 250:
            for x in range(10):
                # part = create_image(40, 40, 4)
                for y in range(2):
                    # part = create_image(25, 25, 4)
                    part = create_image(digitSize, digitSize, 4)
                    img_pil = Image.fromarray(part)
                    draw = ImageDraw.Draw(img_pil)
                    
                    if y:
                        randColor = random.randrange(20)
                        b, g, r, a = 10 + randColor, 50 + randColor, 10 + randColor, 0
                        randX = random.choice(widthItemsBack)
                    else:
                        randColor = random.randrange(-60, 60)
                        if randColor == 54:
                            b, g, r, a = 20, 20, 255, 0
                        else:
                            b, g, r, a = 60 + randColor, 180 + randColor, 60 + randColor, 0
                        randX = random.choice(widthItems)
                    
                    # create new characters in the top of the image
                    randY = random.randrange(round(height*0.15))
                    # randY = random.randrange(height)
                    
                    sign = random.choice(list(chinesseChars))
                    draw.text((0, 0), sign, font = font, fill = (b, g, r, a))
                    part = np.array(img_pil)
                    
                    if y:
                        newParts.append((part, (randX, randY)))
                    else:
                        newParts.append((part, (randX, randY)))
                   
                   
        # THAT WORKS AS I WAS EXPECTED
        # move image
        # draw new parts
        # mask with gradient mask
        # show image
        
        img = np.concatenate((line_with_fixed_height, img[:height - fixed_height, :]))
        limit = round(0.85 * len(newParts))        # this makes funny effect
        
        for key, (part, (posx, posy)) in enumerate(newParts):
            if key < limit:
                # posy += pos * (key+1)
                posy += pos
            else:
                posy = posy
            # if posy > height:
                # del parts[key]
            # else:
                # parts[key] = (part, (posx, posy))     # change value of items in list
            
            now = alpha(part)
            now[np.where(now>0)] += round(45*posy/height)
            # img = paste_image(alpha(part), img, posx, posy)
            img = paste_image(now, img, posx, posy)
            
            
            
        # ************** show created image **************
        # show_image('img', img)
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        pos = 25
        
    cv2.destroyAllWindows()
    
    
    
'''
INFO:
    The cv2.putText don't support no-ascii char in my knowledge. Try to use PIL to draw NO-ASCII(such Chinese) on the image.
    https://stackoverflow.com/questions/50854235/how-to-draw-chinese-text-on-the-image-using-cv2-puttextcorrectly-pythonopen
    
02.09.2019, 23:59
-this is very rubbish for now
    
    
03.09.2019
-think of just moving main screen down and not draw every part each time
    for example:
        img = line_with_fixed_height + img[:width - fixed_height]
        draw new parts
        show image
        
        that's it
        
-other thing is too mask whole screen with gradient image or something like that
-i think it should increase speed, which is very slow because of many useless operations :(

-that works fine
-now think of add some trace after falling characters, which can be generated after random creation of part
    by adding simillar parts with different y_pos and bgr parameters
    
    
-think of create different view (for now there are two planes -> light green on the front and dark green on the bottom)
    their should be moved in x_axis; size of characters may be different too
    
    
'''
