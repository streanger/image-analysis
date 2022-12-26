import sys
from pathlib import Path
import cv2


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
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True


def white_transparent_alpha(img):
    """convert rgb image to rgba image with with alpha channel
    equals 1 for non-white pixels and 0 for white pixels
    https://stackoverflow.com/questions/32290096/python-opencv-add-alpha-channel-to-rgb-image
    """
    # create alpha channel
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
    negated = cv2.bitwise_not(thresh)
    rgba = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    
    # asign mash to alpha channel
    rgba[:, :, 3] = negated
    return rgba


if __name__ == "__main__":
    # read original image
    filename = 'ship_rgb.png'
    if not Path(filename).is_file():
        print('file does not exists: {}'.format(filename))
        sys.exit()
    img = cv2.imread(filename)

    # convert to rgba
    rgba = white_transparent_alpha(img)

    # show for debug
    show_image('rgba', rgba)

    # write image with alpha channel to file
    cv2.imwrite('ship.png', rgba)
