from paddleocr import PaddleOCR
import os
import pymysql
import image as im

ocr = PaddleOCR(use_gpu=False, use_angle_cls=True)


im.image_normalization('E:\PaddleOCR\img', 'E:\PaddleOCR\image')
file_info = os.walk('E:\PaddleOCR\image')
result = []

db = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='Xujiachen@123456',
                    database='tryocr1'
)
cursor = db.cursor()
for root, dirs, files in file_info:
    for file in files:
        img_path = root+'/'+file
        print(img_path)
        x = ocr.ocr(img_path, det=False, cls=True)
        result.append(x)

        try:
            sql = "insert into paddle_rec_only (pic_name, email) VALUES (%s, %s);"
            args = (file, x[0][0])
            cursor.execute(sql, args)
            db.commit()
        except:
            sql = "update paddle_rec_only set email = %s where pic_name = %s"
            args = (x[0][0], file)
            cursor.execute(sql, args)
            db.commit()
cursor.close()
db.close()
for res in result:
    print(res)