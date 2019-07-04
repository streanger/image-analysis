''' script for concatenating many images of messages to one big '''
import sys
import os
import requests
from bs4 import BeautifulSoup as bs
import lxml
from PIL import Image
from io import BytesIO, StringIO

import numpy as np
import cv2

def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def get_content(url=''):
    res = requests.get(url)
    content = res.text
    status = res.status_code
    return content, status
    
    
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
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def save_images(images, prefix=''):
    '''
    for key, link in enumerate(image_list):
        print(link)
        r = requests.get(link)
        with open('image_{}.jpg'.format(key), 'wb') as f:
            f.write(r.content)
    '''
    for key, img in enumerate(images):
        file = '{}image_{}.jpg'.format(prefix, key)
        cv2.imwrite(file, img)
        print(file + ' saved')
    return True
    
    
def url_to_image(url):
    ''' https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/ '''
    # download the image, convert it to a NumPy array, and then read it into OpenCV format
    if False:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
    else:
        r = requests.get(url)
        image = np.asarray(bytearray(r.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image
    
    
def cut_headers(images):
    ''' cut top and bottom header '''
    out = [item[70:-81, :] for item in images]
    return out
    
    
def search_and_cut(images):
    ''' find the position and paste it there '''
    out = []
    for key, image in enumerate(images[:-1]):
        ''' create temp from the following image '''
        template = images[key+1][0:30, :]
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # show_image("template", template)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(grey, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.93
        
        loc = np.where(res >= threshold)
        for index, pt in enumerate(zip(*loc[::-1])):
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (155,255,155), 1)
            # show_image("image_{}".format(key), image)
            crop = image[0:pt[1], :]
            if crop.any():
                out.append(crop)
            else:
                print("empty image: {}".format("image_{}.jpg".format(key)))
            break
        else:
            out.append(image)
            
    if len(images):
        out.append(images[-1])      # think of different way to solve it
    return out
    
    
if __name__ == "__main__":
    script_path()
    data, status = get_content('http://some.page.with.hrefs')
    soup = bs(data, 'lxml')
    links = [link['href'] for link in soup.find_all('a', href=True) if 'some_pattern' in link['href']]
    
    images = [url_to_image(link) for link in links]     # read to memory from url
    
    converted = cut_headers(images)
    out = search_and_cut(converted)                     # do all the stuff
    full_image = np.concatenate(out, axis = 0)
    cv2.imwrite('full_image.jpg', full_image)
    
    
'''
info:
    -threshold is important. At 0.80 level is quite enough
    -this line too --> template = images[key+1][0:40, :]
    -and cut_headers function. For some images we don't need to cut headers. In such situation we can make this line like this:
        --> out = [item[0:-1, :] for item in images]
    -to be honest, for most cases we need to specify our own values :<
'''
