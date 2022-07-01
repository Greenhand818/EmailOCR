import os
import cv2 as cv
import pymysql

Parameters = {
    "target_path": r"E:\GenerateImage\train_data\rec",
    "raw_path": r"E:\GenerateImage\raw_data",
    "list_path": r"E:\GenerateImage\train_data"
}

db_info = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Xujiachen@123456',
            'database': 'tryocr1'
}

def data_reader(target_path, raw_path, list_path, db_info):
    train_path = os.path.join(target_path, "train")
    test_path = os.path.join(target_path, "test")
    train_list = []
    test_list = []

    db = pymysql.connect(
        host=db_info["host"],
        user=db_info["user"],
        password=db_info["password"],
        database=db_info["database"]
    )
    cursor = db.cursor()

    pic_p = os.listdir(raw_path)
    count = 0
    for pic in pic_p:
        path = os.path.join(raw_path, pic)
        img = cv.imread(path)
        sql = "select email from dealt_pic_data where pic_name = %s"
        args = (pic)
        cursor.execute(sql, args)
        x = cursor.fetchone()
        if count % 10 == 0:
            if os.path.exists(os.path.join(test_path, pic)):
                os.remove(os.path.join(test_path, pic))
            cv.imwrite(os.path.join(test_path, pic), img)
            detail_line = "rec/test/" + pic
            detail_line = detail_line + "\t" + x[0] + '\n'
            test_list.append(detail_line)
        else:
            if os.path.exists(os.path.join(train_path, pic)):
                os.remove(os.path.join(train_path, pic))
            cv.imwrite(os.path.join(train_path, pic), img)
            detail_line = "rec/train/" + pic
            detail_line = detail_line + "\t" + x[0] + '\n'
            train_list.append(detail_line)
        count += 1
    cursor.close()
    db.close()

    with open(os.path.join(list_path, "test_list.txt"), 'w') as f:
        f.seek(0)
        f.truncate()
        for t in test_list:
            f.write(t)
    with open(os.path.join(list_path, "train_list.txt"), 'w') as f:
        f.seek(0)
        f.truncate()
        for tr in train_list:
            f.write(tr)




if __name__ == "__main__":
    data_reader(Parameters["target_path"], Parameters["raw_path"], Parameters["list_path"], db_info)