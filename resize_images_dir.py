import sys
import os
from pathlib import Path
from PIL import Image
from rich import print


def script_path():
    """set current path to script path"""
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def resize_image(img, ratio):
    init_width, init_height = img.size
    print('    init: {}'.format((init_width, init_height)))
    new_width = round(init_width*ratio)
    new_height = round(init_height*ratio)
    print('    new: {}'.format((new_width, new_height)))
    img = img.resize((new_width, new_height))
    return img
    
    
if __name__ == "__main__":
    script_path()

    # ******* list files *******
    input_dir = Path('images')
    output_dir = Path('images_resized')
    output_dir.mkdir(exist_ok=True)
    files = [input_dir.joinpath(item) for item in os.listdir(input_dir)]

    # ******* resize & save *******
    ratio = 0.5
    for index, filename in enumerate(files):
        print('{}) {}'.format(index+1, filename))
        img = Image.open(filename)
        resized = resize_image(img, ratio)
        new_path = output_dir.joinpath(filename.name)
        resized.save(new_path)
        print('    {}'.format(new_path))
        print()
        # input()
