import os
import cv2 as cv

Path_Parameter = {
    "raw_path": r"E:\NewAttention_CTCOCR\new_data",
    "target_path": r"E:\environment\PaddleOCR\ocr_recognition",
    "list_path": r"E:\environment\PaddleOCR\ocr_recognition"
}

def pic_to(raw_path, target_path, list_path):
    train_list = list_path+r"\train_data.txt"
    test_list = list_path+r"\test_data.txt"
    train_path = os.path.join(target_path, "train_images")
    path = os.listdir(train_path)
    for x in path:
        p = os.path.join(train_path, x)
        os.remove(p)
    # max = 0
    with open(train_list, 'r') as f:
        for line in f:
            info = line.strip().split(' ')
            train_data = os.path.join(raw_path, info[2])
            train_path0 = os.path.join(train_path, info[2])
            img = cv.imread(train_data)
            cv.imwrite(train_path0, img)

    test_path = os.path.join(target_path, "test_images")
    path = os.listdir(test_path)
    for x in path:
        p = os.path.join(test_path, x)
        os.remove(p)
    with open(test_list, 'r') as f:
        for line in f:
            info = line.strip().split(' ')
            test_data = os.path.join(raw_path, info[2])
            test_path0 = os.path.join(test_path, info[2])
            img = cv.imread(test_data)
            # if max < wide:
            #     max = wide
            cv.imwrite(test_path0, img)
    # print(max)

pic_to(Path_Parameter["raw_path"], Path_Parameter["target_path"], Path_Parameter["list_path"])