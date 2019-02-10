''' script for mask image '''

import os
import sys
import time
import pprint
from collections import Counter
import codecs

import numpy as np
import cv2

# download avatars images
import shutil
import requests
import bs4 as bs
import lxml
import urllib.parse


def script_path():
    '''change current path to script one'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
# *******************************************************************************
# ********************** functions for downloading avatars **********************
# *******************************************************************************


def simple_read(file):
    '''simple_read data from specified file'''
    with codecs.open(file, "r", encoding="utf-8", errors='ignore') as f:
        content = f.read()
    return content
    
    
def get_content(url):
    res = requests.get(url)
    content = res.text
    status = res.status_code
    return content, status
    
    
def make_dir(new_dir):
    ''' make new dir, switch to it and retur new path '''
    current_path = script_path()
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(current_path, new_dir)
    return new_path
    
    
def convert_nick_str_to_list(nick_str):
    nick_str = nick_str.replace("@", " ")
    nick_str = nick_str.replace(",", " ")
    nick_list = [item.strip() for item in nick_str.split() if item]
    to_call = " ".join(["@" + item for item in nick_list])
    return nick_list, to_call
    
    
def get_avatar(nick):
    base_url = "https://www.wykop.pl/ludzie/"
    nick_url = urllib.parse.urljoin(base_url, nick)
    content, status = get_content(nick_url)
    if status == 404:
        return ""
    soup = bs.BeautifulSoup(content, 'lxml')
    hrefs = soup.find_all('img', {'title': nick})       #this is useful
    if hrefs:
        avatar_url = hrefs[0]['src']
    else:
        avatar_url = ""
    return avatar_url
    
    
def download_image(url, file_name):
    '''download image from specified url and save it to specified file_name'''
    try:
        response = requests.get(url, stream=True)
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        return False
        
        
def download_avatars(nicknamesList, dirToSave):
    new_path = make_dir(dirToSave)                              #create dir if not exists
    for nick in nicknamesList:
        avatar_url = get_avatar(nick)
        file_path = os.path.join(new_path, nick + ".jpg")
        if download_image(avatar_url, file_path):
            print("avatar saved as: {}".format(file_path))
        else:
            print("failed to download from: '{}' nick: '{}'".format(avatar_url, nick))
    return True
    
    
def dir_files(dir, full=False):
    ''' return list of full path of files from specified dir '''
    if full:
        return [os.path.abspath(os.path.join(dir, file)) for file in os.listdir(dir)]
    else:
        return [file for file in os.listdir(dir)]

        
# *******************************************************************************
# **********************  functions for making image mask  **********************
# *******************************************************************************


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
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def mask_image(img, mask, value):
    ''' value: 0-100 '''
    return True
    
    
def cat_multi_images(imagesList):
    ''' list of lists with images '''
    lines = []
    for row in imagesList:
        lines.append(np.concatenate(([avatar for avatar in row]), axis=1))
    out = np.concatenate(([line for line in lines]), axis=0)
    return out
    
    
def calc_items(big, small):
    ''' if size doesn't fit just append column or row, but here just return info '''
    itemsNumber = big//small
    appendLine = False
    if (big - itemsNumber*small > 0):
        appendLine = True
    return itemsNumber, appendLine
    
    
def repeat_list(l, number):
    ''' increase number of element in list to specified size '''
    multi = (number//len(l)) + 1
    resized = (l*multi)[:number]
    return resized
    
    
def create_image():
    img = np.array(range(225), dtype=np.uint8).reshape((15, 15))        # create one layer array
    row = np.concatenate(([img for x in range(20)]), axis=1)
    out = np.concatenate(([row for x in range(20)]), axis=0)
    out = np.stack((out,)*3, axis=-1)                                   # convert 1 layer to 3 layer (gray -> rgb)
    return out
    
    
def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        val = func(*args, **kwargs)
        after = time.time()
        print("elapsed time: {}s".format(after-before))
        return val
    return f
    
    
def usage():
    print("usage of mask_image_with_other.py script")
    print("     python <script> <file_with_avatars.txt> <mask_image.xxx>")
    print("     python <script> <directory_with_avatars> <mask_image.xxx>")
    print()
    print("for now use file avatars.txt, directory avatars, mask.jpg, and output.jpg")
    return True
    
    
@timer
def main(args):
    '''
    if not args:
        usage()
        return False
    else:
        if not (len(args) > 1):
            print("not enough arguments: {}, needed 2".format(len(args)))
            return False
        arg0, arg1 = args[:2]
        if arg0.endswith('.txt'):
            print("from .txt file with nicknames")
        else:
            print("from directory with images")
        return False
    '''
    
    maskFile = 'mask.jpg'
    
    
    # ***********************************************************************
    # **********************  download avatars images  **********************
    # ***********************************************************************
    
    
    if False:
        nicknamesList, _ = convert_nick_str_to_list(simple_read('avatars.txt'))
        nicknamesList.sort()
        
        # get the list of current files to avoid redundancy
        try:
            currentAvatars = [os.path.splitext(item)[0] for item in dir_files('avatars', full=False)]
            currentAvatars.sort()
        except:
            currentAvatars = []
        
        diff = set(currentAvatars).symmetric_difference(set(nicknamesList))     # download only missing avatars
        pprint.pprint("len(diff): {}, diff: {}".format(len(diff), diff))
        download_avatars(diff, "avatars")
        sys.exit()
    
    # *************************************************************************    
    # **********************  create image from avatars  **********************
    # *************************************************************************
    
    avatarsList = dir_files('avatars', full=True)
    # avatarsList = avatarsList[:400]
    avatarsImages = [cv2.imread(file, 1) for file in avatarsList]
    
    # get the most common shape of avatars
    avatarsShapes = [item.shape[:2] for item in avatarsImages]
    mostCommonShape = Counter(avatarsShapes)
    avY, avX = mostCommonShape.most_common(1)[0][0]
    
    # if some of avatars isnt the same size as others, just shrink it
    for key, avatar in enumerate(avatarsImages):
        avatarY, avatarX, _ = avatar.shape
        if (avatarY, avatarX) != (avY, avX):
            background = np.zeros((avY, avX, 3), dtype=np.uint8)
            # print("{} avatar's shape is not correct: {}".format(key, avatar.shape[:2]))
            avatar = avatar[:avY, :avX]                             # shrink to wanted size
            currentY, currentX, _ = avatar.shape                    # check what we've got
            background[:currentY, :currentX] = avatar
            avatarsImages[key] = background
            
    # read the mask image into memory
    mask = cv2.imread(maskFile, 1)
    maskY, maskX, _ = mask.shape
    
    # it is swapped -> colItems x appendRow
    colItems, appendCol = calc_items(maskX, avX)
    rowItems, appendRow = calc_items(maskY, avY)
    itemsNeeded = rowItems*colItems
    
    # repeat images in list
    repeatedAvatars = repeat_list(avatarsImages, itemsNeeded)
    print(len(repeatedAvatars))
    # sys.exit()
    
    avatarsRows = [repeatedAvatars[n:n+colItems] for n in range(0, itemsNeeded, colItems)]
    if appendRow:
        avatarsRows.insert(len(avatarsRows), avatarsRows[0])
    if appendCol:
        avatarsRows = [row + [row[0]] for row in avatarsRows]
    out = cat_multi_images(avatarsRows)
    imageFromAvatars = out[:maskY, :maskX]                      # fitToMask
    
    
    # ***************************************************************
    # **********************  mask two images  **********************
    # ***************************************************************
    
    # last thing todo is to mask image; avatars image -> imageFromAvatars; mask image -> mask
    
    if False:
        for alpha in np.arange(0, 1.0, 0.05):
            print("alpha: {}".format(alpha), end='\r', flush=True)
            output = mask.copy()
            overlay = imageFromAvatars.copy()
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
            cv2.imwrite("output{}.jpg".format(alpha), output)
            
            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            cv2.imshow("output", output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.001)
        cv2.destroyAllWindows()
    else:
        output = mask.copy()
        overlay = imageFromAvatars.copy()  
        alpha = 0.1
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
        cv2.imwrite("output2.jpg", output)
        # show_image("output, alpha: {}".format(alpha), output)
        
    return True
    
    
if __name__ == "__main__":
    current_path = script_path()
    main(sys.argv[1:])

'''
todo:
    -think of resizing mask if sum of avatars is more than mask size
    -add some args as in usage
    -clean module import
    -think of separate downloading avatars images to other script
    -
'''
