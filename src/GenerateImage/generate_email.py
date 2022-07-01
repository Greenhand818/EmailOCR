import os
import numpy as np
import cv2 as cv
import random
import pymysql

Parameters = {
    "email_suffix": "E:\GenerateImage\email_suffix.txt",
    "letter_path": "E:\GenerateImage\letters",
    "target_path": r"E:\GenerateImage\raw_data"
}

sql_info = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Xujiachen@123456',
            'database': 'tryocr1'
}

match = {
    'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L',
    'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
    'y': 'Y', 'z': 'Z', '@': '@', '_': '_', '.': 'dot', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S',
    'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z', '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
}

def generate_pic(email, pic_name):  ### 生成图片
    words = list(email)
    print(words)
    length = len(email)
    img = np.zeros((40, 24*length, 3), np.uint8)
    wide = 0
    for word in words:
        lp = os.path.join(Parameters["letter_path"], match[word])
        if word >= 'a' and word <= 'z':
            lp = os.path.join(lp, "lower")
        elif word >= 'A' and word <= 'Z':
            lp = os.path.join(lp, "capital")
        lpOne = os.path.join(lp, os.listdir(lp)[random.randint(0, len(os.listdir(lp))-1)])
        letter_img = cv.imread(lpOne)
        blank = True
        x = [0, letter_img.shape[1]]
        count = 0
        for width in range(letter_img.shape[1]):
            if blank == True:
                for height in range(letter_img.shape[0]):
                    if letter_img[height][width][0] != 255:
                        x[count] = width
                        count += 1
                        blank = False
                        break
            else:
                blank = True
                for height in range(letter_img.shape[0]):
                    if letter_img[height][width][0] != 255:
                        blank = False
                        break
                if blank == True:
                    x[count] = width
                    break
        # print(x)
        img[0:40, wide:wide+x[1]-x[0]] = letter_img[0:40, x[0]:x[1]]
        wide += x[1] - x[0]
    # cv.imshow('1', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    ipath = os.path.join("./raw_data",  pic_name)
    if os.path.exists(ipath):
        os.remove(ipath)
    cv.imwrite(ipath, img)

def generate(suffix_path, sql_info, amount):
    db = pymysql.connect(
        host=sql_info["host"],
        user=sql_info["user"],
        password=sql_info["password"],
        database=sql_info["database"]
    )
    words = []
    pic_name = []
    with open(suffix_path, encoding='utf-8') as suffix_f:
        email_suffix = suffix_f.read()
        suffix = email_suffix.split()
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
            key = random.sample(match.keys(), 1)
            if key[0] != '@':
                if j == 0:
                    if key[0] != '_' and key[0] != '.':
                        word.append(key[0])
                        index.append(match[key[0]])
                    else:
                        j -= 1
                else:
                    word.append(key[0])
                    index.append(match[key[0]])
            else:
                j -= 1
        for k in suffix[email_index]:  ### @之后部分
            word.append(k)
            index.append(match[k])
        words.append("".join(word))
        print(words[i])  ### 生成的字符串
        print(index)  ### 字典索引
        pic_name.append("%d.jpg" % i)  ### 生成图片文件名
        print(pic_name[i])
        generate_pic(words[i], pic_name[i])
        try:
            sql = "insert into predict_pic (pic_name, email) values (%s, %s)"
            args = (pic_name[i], words[i])
            cursor.execute(sql, args)
            db.commit()
        except:
            sql = "update predict_pic set email = %s where pic_name = %s"
            args = (words[i], pic_name[i])
            cursor.execute(sql, args)
            db.commit()
        cursor.close()
    db.close()

if __name__ == "__main__":
    generate(Parameters["email_suffix"], sql_info, 10)
