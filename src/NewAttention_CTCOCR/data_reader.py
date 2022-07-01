import os

Parameters = {
    "target_path": r"E:\environment\PaddleOCR\train_data\rec",
    "label_path": r"E:\environment\PaddleOCR\ocr_recognition",
    "dict_path": r"E:\NewAttention_CTCOCR\chinese_cht_dict.txt"
}


def deal_label(label_text):
    pic = []
    label = []
    with open(label_text, 'r') as f:
        for lines in f:
            line = lines.strip().split()
            pic.append(line[2])
            lab = line[3].split(",")
            Lab = []
            for l in lab:
                Lab.append(small_dic[int(l)])
            label.append("".join(Lab))
    detail = []
    for i in range(len(pic)):
        detail.append(pic[i] + '\t' + label[i] + '\n')
    return detail


with open(Parameters["dict_path"], encoding='utf-8') as dic_f:
    chinese_dic = dic_f.read()
    letter = chinese_dic.split()
    small_dic = {}
    count = 0
    for s in letter:
        if count == 13 or count == 62 or (count >= 15 and count <= 24) or (count >= 31 and count <= 57) or (
                count >= 64 and count <= 89):
            small_dic[count] = letter[count]
        count += 1
    print(small_dic)


def data_reader(target_path, label_path):
    train_label = os.path.join(label_path, "train_data.txt")
    test_label = os.path.join(label_path, "test_data.txt")
    save_train_label = os.path.join(target_path, "rec_gt_train.txt")
    save_test_label = os.path.join(target_path, "rec_gt_test.txt")
    deal_label(train_label)
    detail_train = deal_label(train_label)
    detail_test = deal_label(test_label)
    with open(save_test_label, 'w') as f:
        f.seek(0)
        f.truncate()
        for line in detail_test:
            f.write("rec/test/" + line)

    with open(save_train_label, 'w') as f:
        f.seek(0)
        f.truncate()
        for line in detail_train:
            f.write("rec/train/" + line)


if __name__ == '__main__':
    data_reader(Parameters["target_path"], Parameters["label_path"])
