import functions as fn
import numpy as np

from PIL import Image, ImageFilter, ImageTk
import tkinter as tk
import os 
from os.path import isfile, join
from os import listdir
from time import time


path_1 = 'Input/'
onlyfiles = [f for f in listdir(path_1) if isfile(join(path_1, f))]
path_1 = path_1 + onlyfiles[0]

my_image = fn.open_image(path_1)
imageArray = np.asarray(my_image)

print('\n'*3)


path = 'Images\\Crop\\'

#Image options
def mosaics():
    time_start = time()
    avg_dic = fn.average_pixel_dic(path)
    time_end = time()
    timing = time_end - time_start
    print('average_pixel_dic time:', timing)
    image_arr_working = fn.process_image(imageArray, avg_dic, 100, path)
    new_final_image = Image.fromarray(image_arr_working)
    new_final_image.show()


def contour():
    out = my_image.filter(ImageFilter.CONTOUR)
    out.show()


def emboss():
    out = my_image.filter(ImageFilter.EMBOSS)
    out.show()

#display image in tkinter
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
#set buttons height and width
but_ht_wd = {'height' : 1, 'width' : 10}
#Mosaic option
disp_mosaic = tk.Button(frame, text = 'Mosaic', command = mosaics, **but_ht_wd)
disp_mosaic.pack(anchor=tk.W)
#Blur option
disp_contur = tk.Button(frame, text = 'Contour', command = contour, **but_ht_wd)
disp_contur.pack(anchor=tk.W)
#Emboss option 
disp_contur = tk.Button(frame, text = 'Emboss', command = emboss, **but_ht_wd)
disp_contur.pack(anchor=tk.W)

root.mainloop()