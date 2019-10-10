from PIL import Image
import numpy as np
from os.path import isfile, join
from os import listdir
import math as mt
from time import time
import json

def cut_image(image_arr, cut_size):
    #copy so the assignment is possible
    image_arr_working = image_arr.copy()
    #take shape values
    columns = np.shape(image_arr)[1]
    rows = np.shape(image_arr)[0]

    for i in range(0, columns, cut_size):
        for k in range(0, rows, cut_size):
            #check the shape of square
            shape = np.shape(image_arr_working[:, i : i + cut_size][k : k + cut_size])
            #get average pixel RGB value
            avg_val =avg_pixel(image_arr_working[:, i : i + cut_size][k : k + cut_size])
            #multiply data
            new_arr = np.reshape(avg_val*shape[0]*shape[1], shape)
            #assign
            image_arr_working[:, i : i + cut_size][k : k + cut_size] = new_arr
    return image_arr_working


def process_image(image_arr, avg_dic, cut_size, path):
    time_st = time()
    #copy so the assignment is possible
    image_arr_working = image_arr.copy()
    #take shape values
    columns = np.shape(image_arr)[1]
    rows = np.shape(image_arr)[0]

    for i in range(0, columns, cut_size):
        for k in range(0, rows, cut_size):
            #check the shape of square
            shape = np.shape(image_arr_working[:, i : i + cut_size][k : k + cut_size])
            #get average pixel RGB value
            avg_val =avg_pixel(image_arr_working[:, i : i + cut_size][k : k + cut_size])
            #get image from list
            name = find_close(avg_val, avg_dic)
            #resize the image
            size = shape[1], shape[0]
            batch_img = resize_img(name, size, path)
            # assign
            image_arr_working[:, i : i + cut_size][k : k + cut_size] = batch_img
    time_en = time()
    timing = time_en - time_st
    print('process_image time:', timing)
    return image_arr_working


def resize_img(name, size, path):
    my_image = open_image(path+name)
    new_my_image = my_image.resize(size)
    new_my_image = np.asarray(new_my_image)
    return new_my_image


def open_image(path):
    try:
        my_image = Image.open(path)
    except:
        print('Unable to load image\n'+path)
    return my_image


def avg_pixel(image_arr):
    red = 0
    green = 0
    blue = 0
    count_pixel = 0
    for line in image_arr:
        for pixel in line:
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]

            count_pixel += 1
    avg_red = int(round(red/count_pixel))
    avg_green = int(round(green/count_pixel))
    avg_blue = int(round(blue/count_pixel))
    return avg_red, avg_green, avg_blue


def average_pixel_dic(image_path):
    
    onlyfiles = [f for f in listdir(image_path) if isfile(join(image_path, f))]
    #load cache from file, create dictionary if there is no cache
    json_path = 'Cache\\cache.txt'

    try:
        with open(json_path) as json_cache:
            avg_dic = json.load(json_cache)
    except IOError as error_1:
            avg_dic = {}

    for i in onlyfiles:
        #check if 'i' not is in the cache
        if i not in avg_dic:
        #no -> open file, calc avg, add avg to dictionary
            try:
                my_crop_image = Image.open(image_path+i)
            except IOError as error_2:
                print('Unable to load image', i)
            else:
                my_crop_image = np.asarray(my_crop_image)
                avg_dic[i] = avg_pixel(my_crop_image)
    #update the cache
    with open(json_path, 'w') as out_json_cache:
        json.dump(avg_dic, out_json_cache)
    #return the cache
    return avg_dic


def find_close(image_avg, image_avg_dic):
    #set dummy key and max value to set the variables
    im_key = 'Start_key'
    im_value = mt.sqrt(255**2 + 255**2 + 255**2)
    for key, value in image_avg_dic.items():
        #calculate distance
        Red_dist = value[0] - image_avg[0]
        Green_dist = value[1] - image_avg[1]
        Blue_dist = value[2] - image_avg[2]
        distance = mt.sqrt(Red_dist**2 + Green_dist**2 + Blue_dist**2)
        #store the closest
        if im_value > distance:
            im_value = distance
            im_key = key
    return im_key



if __name__ == '__main__':
    print('This is a functions module')