#!/usr/bin/python3
"""adhoc script for specific border drawing"""
import sys
import os
import time
from pathlib import Path
import cv2
import numpy as np


def script_path():
    """set current path to script path"""
    current_path = str(Path(__file__).parent)
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
def margin(img, space_size, color=(0, 0, 0)):
    """space_size -integer; 2 is the lowest value for proper read; try to increase value and look for decoding time"""
    shape = img.shape
    if len(shape) == 2:
        current_h, current_w = img.shape
        new_shape = (current_h+space_size*2, current_w+space_size*2)
    else:
        current_h, current_w, layers = shape
        new_shape = (current_h+space_size*2, current_w+space_size*2, layers)
        
    new_image = np.ones(new_shape, dtype=np.uint8)*color
    new_image[space_size:-space_size, space_size:-space_size] = img
    return new_image
    
    
def crop_to_contour(img, on_white=True, shift_corner=False):
    """crop image to the first contour"""
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if on_white:
        grey = cv2.bitwise_not(grey)
    ret, thresh = cv2.threshold(grey, 1, 255, cv2.THRESH_BINARY)  # ORIGINAL
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    first = contours[0]
    transposed = first.transpose()
    xmin, xmax = transposed[0].min(), transposed[0].max()
    ymin, ymax = transposed[1].min(), transposed[1].max()
    print(xmin, xmax, ymin, ymax)
    if shift_corner:
        cropped = img[ymin+1:ymax, xmin+1:xmax]  # DEBUG
    else:
        cropped = img[ymin:ymax, xmin:xmax]
    return cropped
    
    
def transparent_alpha(img, on_white=True):
    """convert rgb image to rgba image with with alpha channel
    equals 1 for non-white pixels and 0 for white pixels
    https://stackoverflow.com/questions/32290096/python-opencv-add-alpha-channel-to-rgb-image
    """
    # create alpha channel
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # decrease or increase lower bound for your needs
    if on_white:
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    else:
        ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    
    # add alpha channel
    rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    
    # asign mash to alpha channel
    if on_white:
        negated = cv2.bitwise_not(thresh)
        rgba[:, :, 3] = negated
    else:
        rgba[:, :, 3] = thresh
    return rgba
    
    
def remove_center_line(img):
    width = img.shape[1]
    if width%2:
        center_line_pos = (width-1)//2
        img = np.concatenate((img[:, :center_line_pos], img[:, center_line_pos+1:]), axis=1)
    return img
    
    
if __name__ == "__main__":
    script_path()
    
    filename = 'image-rgba.png'
    out = str(Path(filename).with_stem(Path(filename).stem + '-border'))
    img = cv2.imread(filename, 0)  # read in greyscale
    img = margin(img, 100, color=0)
    
    # colors
    grey = (150, 150, 150)
    green = (20, 255, 70)
    
    # ******* 1st time contours *******
    # threshold
    blur = cv2.blur(img, (3, 3))  # blur the image to reduce noise
    ret, thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY)
    
    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # blank drawing
    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
    
    # draw contours
    contour = contours[0]
    cv2.drawContours(drawing, contours, 0, green, -1, cv2.LINE_AA, hierarchy)
    cv2.drawContours(drawing, contours, 0, green, 2, cv2.LINE_AA, hierarchy)  # DEBUG
    
    
    # ******* 2nd time contours *******
    # threshold
    img = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(img, (3, 3))  # blur the image to reduce noise
    ret, thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY)
    
    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # blank drawing
    on_white = False
    if on_white:
        drawing = np.ones((thresh.shape[0], thresh.shape[1], 3), np.uint8)
        drawing *= 255
    else:
        drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
        
    # draw final contours
    contour = contours[0]
    cv2.drawContours(drawing, contours, 0, green, 2, cv2.LINE_AA, hierarchy)
    
    # ******* blur, crop to contour & transparent *******
    blurred = cv2.blur(drawing, (2, 2))
    cropped = crop_to_contour(blurred, on_white=on_white, shift_corner=True)
    img_rgba = transparent_alpha(cropped, on_white=on_white)
    img_rgba = remove_center_line(img_rgba)
    cv2.imwrite(out, img_rgba)
    