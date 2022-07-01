import random
import pymysql
import cv2 as cv
import numpy as np

Parameters = {
    "raw_data_path": r"E:\NewAttention_CTCOCR\new_data",
    "train_path": r"E:\environment\PaddleOCR\ocr_recognition\train_images",
    "test_path": r"E:\environment\PaddleOCR\ocr_recognition\test_images",
    "train_list": r"E:\environment\PaddleOCR\ocr_recognition\train_data.txt",
    "test_list": r"E:\environment\PaddleOCR\ocr_recognition\test_data.txt",
    "dict_path": r"E:\NewAttention_CTCOCR\chinese_cht_dict.txt"
}



dic_f = open(Parameters["dict_path"], encoding='utf-8')
chinese_dic = dic_f.read()
letter = chinese_dic.split()
small_dic = {}
count = 0
for s in letter:
    if count == 13 or count == 62 or (count >= 15 and count <= 24) or (count >= 31 and count <= 57) or (
            count >= 64 and count <= 89):
        small_dic[letter[count]] = count
    count += 1
print(small_dic)
dic_f.close()


def generate_pic(words, path, pic_name):  ### 生成图片
    try:
        img = cv.imread(path)

        font = random.randint(0, 7)
        scale = cv.getTextSize(words, font,  1, 1)
        img = cv.resize(img, (scale[0][0], 36))
        img = cv.putText(img, words, (0, (scale[0][1]+2)), font, 1, (0, 0, 0))
        print(scale)
        ipath = "./new_data/" + pic_name
        cv.imwrite(ipath, img)
    except:
        return False
    return img.shape


def generate(dictionary, amount, path):  ### 生成list文件及图片
    try:
        train_list = []
        test_list = []
        words = []
        pic_name = []
        suffix_f = open(path, encoding='utf-8')
        email_suffix = suffix_f.read()
        suffix = email_suffix.split()
        suffix_f.close()

        db = pymysql.connect(
            host='localhost',
            user='root',
            password='Xujiachen@123456',
            database='tryocr1'
        )

        for i in range(amount):
            cursor = db.cursor()
            word = []
            index = []
            length = random.randint(4, 18)
            suffix_len = len(suffix)
            email_index = random.randint(0, suffix_len - 1)
            # print(length)
            # print(i)
            for j in range(length):  ### @之前部分
                key = random.sample(dictionary.keys(), 1)
                if key[0] != '@':
                    if j == 0:
                        if key[0] != '_' and key[0] != '.':
                            word.append(key[0])
                            index.append(dictionary[key[0]])
                        else:
                            j -= 1
                    else:
                        word.append(key[0])
                        index.append(dictionary[key[0]])
                else:
                    j -= 1
            for k in suffix[email_index]:  ### @之后部分
                word.append(k)
                index.append(dictionary[k])
            words.append("".join(word))
            print(words[i])  ### 生成的字符串
            print(index)  ### 字典索引
            pic_name.append("%d.jpg" % i)  ### 生成图片文件名
            print(pic_name[i])
            height, width, channel = generate_pic(words[i], './fake_bg.jpg', pic_name[i])
            list = str(width) + ' ' + str(height) + ' ' + pic_name[i] + ' '
            x = str(index[0])
            for ind in index:
                if x != str(ind):
                    x = x + ',' + str(ind)
            print(x)
            list = list + x + '\n'
            print(list)
            if i % 10 == 0:
                test_list.append(list)
            else:
                train_list.append(list)

            try:
                sql = "insert into new_data (newpic_name, newpic_raw_label) values (%s, %s)"
                args = (pic_name[i], words[i])
                cursor.execute(sql, args)
                db.commit()
            except:
                sql = "update new_data set newpic_raw_label = %s where newpic_name = %s"
                args = (words[i], pic_name[i])
                cursor.execute(sql, args)
                db.commit()
            cursor.close()
            print("**********************************")

        db.close()
        with open(Parameters["test_list"], 'a') as f1:
            for test_image in test_list:
                f1.write(test_image)

        with open(Parameters["train_list"], 'a') as f2:
            for train_image in train_list:
                f2.write(train_image)
    except:
        raise
    return True

with open(Parameters["train_list"], 'w') as f:
    f.seek(0)
    f.truncate()
with open(Parameters["test_list"], 'w') as f:
    f.seek(0)
    f.truncate()
generate(small_dic, 20000, path='./email_suffix.txt')

