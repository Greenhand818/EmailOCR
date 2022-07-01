import os
import pymysql
import paddlehub as hub
import image as im

def predict_image(path, table, model):
    db1 = pymysql.connect(host='localhost',
                          user='root',
                          password='Xujiachen@123456',
                          database='tryocr1')
    cursor = db1.cursor()
    file_info = os.walk(path)
    ocr = hub.Module(name=model, lang='en', enable_mkldnn=True)
    for root, dirs, filenames in file_info:
        for x in filenames:
            y = [root + '/' + x]
            result = ocr.recognize_text(paths=y)
            if len(result[0]['data']) != 0:
                m = result[0]['data'][0]['text']
            else:
                m = 'null'
            sql = 'SELECT COLUMN_NAME  FROM information_schema.columns WHERE table_name= %s'
            args = (table)
            cursor.execute(sql, args)
            columns = cursor.fetchall()
            # print(columns)
            try:
                sql = "insert into " + table + " (" + columns[0][0] + ", " + columns[1][0] + ") VALUES (%s, %s);"
                args = (x, m)
                cursor.execute(sql, args)
                db1.commit()
                print(x)
            except:
                sql = "update " + table + " set " + columns[1][0] + " = %s where " + columns[0][0] + " = %s;"
                args = (m, x)
                cursor.execute(sql, args)
                db1.commit()
                print(x)
    print('success')
    cursor.close()
    db1.close()

im.image_normalization(r'E:\NewAttention_CTCOCR\new_data', 'E:\PaddleOCR\image')
predict_image('E:\PaddleOCR\image', 'new_paddle_rec_result', "multi_languages_ocr_db_crnn")