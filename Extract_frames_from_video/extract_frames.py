import sys
import os
import cv2

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def extract_frames_from_video(file):
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
        count += 1
        success,image = vidcap.read()
        if count % 2 == 0:                            # half of frames
            success,image = vidcap.read()
            success,image = vidcap.read()
        print('Read a new frame: ', success)
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    videoFile = "video.mp4"
    extract_frames_from_video(videoFile)
    