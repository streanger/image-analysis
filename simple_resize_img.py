import cv2

def simple_resize_img(img, newSize):
    ''' newSize is int type; 0-99 -> resize down; 100 -> the same size; 101+ -> resize up '''
    height = round((img.shape[0])*(newSize/100))
    width = round((img.shape[1])*(newSize/100))
    resized = cv2.resize(img, (width, height))
    return resized
    
if __name__ == "__main__":
    print(42)
