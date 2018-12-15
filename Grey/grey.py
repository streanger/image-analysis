import sys
import os
import cv2
import warnings

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path
    
def make_dir(new_dir):
    ''' make new dir and return new path '''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path
    
    
if __name__ == "__main__":
    warnings.resetwarnings()
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    path = script_path()
    scriptName = os.path.basename(os.path.normpath(sys.argv[0]))
    # print(scriptName)
    if 'all' in scriptName:
        files = [item for item in os.listdir() if item.endswith(('.png', 'jpg', 'jpeg'))]
    else:
        files = [sys.argv[1]]
    new_path = make_dir("grey")
    for file in files:
        file = os.path.basename(os.path.normpath(file))
        img = cv2.imread(file, 0)
        out = os.path.join(new_path, '_grey.'.join(file.split('.')))
        print(out)
        cv2.imwrite(out, img)