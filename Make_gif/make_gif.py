import sys
import os
import imageio

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def make_gif(files):
    with imageio.get_writer('movie.gif', mode='I', fps=60) as writer:
        for file in files:
            image = imageio.imread(file)
            writer.append_data(image)
    return True
    
    
if __name__ == "__main__":
    path = script_path()
    files = [item for item in os.listdir() if item.endswith((".jpg", ".png"))]
    print(files)
    make_gif(files)