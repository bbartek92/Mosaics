import numpy as np
from PIL import Image, ImageFilter
from os.path import isfile, join
from os import listdir

image_path = 'Images\\Raw\\'
onlyfiles = [f for f in listdir(image_path) if isfile(join(image_path, f))]

for i in onlyfiles:
    try:
        my_image = Image.open('Images\\Raw\\'+i)
    except:
        print('Unable to load image', i)
    else:
        if my_image.size[0] < my_image.size[1]:
            ratio = my_image.size[0]
        else:
            ratio = my_image.size[1]
            params =(0, 0, ratio, ratio)
            im_crop = my_image.crop(params)
            im_crop.save('Images\\Crop\\'+i)
