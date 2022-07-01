import os
import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import random
import pymysql

Parameters = {
    "email_suffix": "E:\GenerateImage\email_suffix.txt",
    "target_path": r"E:\GenerateImage\data_pic",
    "ttf_path": r"E:\GenerateImage\ttf"
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

def generate_pic(email, pic_name, target_path, ttf_path):  ### 生成图片
    length = len(email)
    ttf_list = os.listdir(ttf_path)
    ttf = random.sample(ttf_list, 1)
    font = ImageFont.truetype(os.path.join(ttf_path, ttf[0]), 20)
    img = Image.new("RGB", (15 * length, 40), (255, 255, 255))
    image = ImageDraw.Draw(img)
    height, width = img.height, img.width
    area = [1, 1]
    image.text(area, email, font=font, fill="#000000")
    ipath = os.path.join(target_path,  pic_name)
    if os.path.exists(ipath):
        os.remove(ipath)
    img.save(ipath)
    img = cv.imread(ipath)
    source = np.float32([[1, 1], [1, height], [width, height], [width, 1]])
    offset = [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5),
              random.randint(0, 5), 0 - random.randint(0, 5), 0 - random.randint(0, 5), 0 - random.randint(0, 5),
              0 - random.randint(0, 5), 0 - random.randint(0, 5)]

    ### 目标四点定位
    height1 = [height - 5 + offset[random.randint(0, 9)], height - 5 + offset[random.randint(0, 9)],
               5 + offset[random.randint(0, 9)]]
    width1 = [5 + offset[random.randint(0, 9)], width - 5 + offset[random.randint(0, 9)],
              width - 5 + offset[random.randint(0, 9)]]
    dst = np.float32([[5, 5], [width1[0], height1[0]],
                    [width1[1], height1[1]],
                    [width1[2], height1[2]]])
    # 找透视变换区域
    dot = [[5, 5], [width1[0], height1[0]], [width1[1], height1[1]], [width1[2], height1[2]]]
    dot1 = sorted(dot)
    print(dot1)
    line1 = (dot1[1][0] - dot1[0][0], dot1[0][1] - dot1[1][1], dot1[1][1]*dot1[0][0] - dot1[0][1]*dot1[1][0])
    line2 = (dot1[3][0] - dot1[2][0], dot1[2][1] - dot1[3][1], dot1[3][1]*dot1[2][0] - dot1[2][1]*dot1[3][0])

    dot2 = sorted(dot, key=lambda x: x[1])
    print(dot2)
    line3 = (dot2[1][1] - dot2[0][1], dot2[0][0] - dot2[1][0], dot2[1][0] * dot2[0][1] - dot2[0][0] * dot2[1][1])
    line4 = (dot2[3][1] - dot2[2][1], dot2[2][0] - dot2[3][0], dot2[3][0] * dot2[2][1] - dot2[2][0] * dot2[3][1])

    # dst1 = np.float32([[10, 10], [10, 30], [50, 30], [50, 10]])
    target_width = max(width1[1], width1[2])
    target_height = max(height1[0], height1[1])
    ### 变换矩阵
    # cv.imshow("2", img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    M = cv.getPerspectiveTransform(source, dst)
    result = cv.warpPerspective(img, M, (target_width, target_height))
    # 对黑色块区域填白
    h, w = result.shape[0], result.shape[1]
    for x in range(h):
        for y in range(w):
            if ((x * line1[0] + y * line1[1] + line1[2]) * line1[1] <= 0) or ((x * line2[0] + y * line2[1] + line2[2])*line2[1] >= 0) or ((y * line3[0] + x * line3[1] + line3[2])*line3[1] <= 0) or ((y * line4[0] + x * line4[1] + line4[2])*line4[1] >= 0):
                result[x][y] = [255, 255, 255]

    ipath = os.path.join(target_path,  pic_name)
    if os.path.exists(ipath):
        os.remove(ipath)
    cv.imwrite(ipath, result)


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
        generate_pic(words[i], pic_name[i], Parameters["target_path"], Parameters["ttf_path"])
        try:
            sql = "insert into entire_transform (pic_name, email) values (%s, %s)"
            args = (pic_name[i], words[i])
            cursor.execute(sql, args)
            db.commit()
        except:
            sql = "update entire_transform set email = %s where pic_name = %s"
            args = (words[i], pic_name[i])
            cursor.execute(sql, args)
            db.commit()
        cursor.close()

if __name__ == "__main__":
    generate(Parameters["email_suffix"], sql_info, 100)