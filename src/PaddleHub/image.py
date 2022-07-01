import os
import cv2 as cv
import math

def image_normalization(path, save_path):
    file_info = os.walk(path)
    wid = []
    pic_name =[]
    picture = {}
    save_file_info = os.listdir(save_path)
    for save_file in save_file_info:
        save_p = os.path.join(save_path, save_file)
        os.remove(save_p)
    for root, dirs, files in file_info:
        for file in files:
            file_path = root + '/' + file
            pic = cv.imread(file_path)
            height, width, channel = pic.shape
            wid.append(width)
            pic_name.append(file)
            picture[file] = pic
        max = 0
        for w in wid:
            if w > max:
                max = w
        for name in pic_name:
            wide = picture[name].shape[1]
            res_pic = cv.copyMakeBorder(picture[name], 0, 0, 5, max-wide, cv.BORDER_CONSTANT, value=(255, 255, 255))
            cv.imwrite(save_path+'/'+name, res_pic)
