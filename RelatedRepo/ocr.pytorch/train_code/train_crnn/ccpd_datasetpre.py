import sys
import os
from sklearn.utils import shuffle

ccpd_path = '/data/OpenSourceDatasets/CCPD2019/'
provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
             'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
             'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']


def generate_train_dataset():
    dir_list = os.listdir(ccpd_path)
    all_names = []
    for dir in dir_list:
        jpg_names = os.listdir(ccpd_path + dir)
        for jpg_name in jpg_names:
            all_names.append(ccpd_path + dir + '/' + jpg_name)
    train_length = int(len(all_names) * 0.7)
    all_names = shuffle(all_names)
    train_names = all_names[:train_length]
    valid_names = all_names[train_length:]
    f = open('train.txt', 'w')
    for train_name in train_names:
        plate_numbers = generate_chars(train_name)
        to_write = train_name + '\t'+ plate_numbers
        f.write(to_write)
        f.write('\n')
    f.close()
    f = open('valid.txt', 'w')
    for valid_name in valid_names:
        plate_numbers = generate_chars(valid_name)
        to_write = valid_name + '\t' + plate_numbers
        f.write(to_write)
        f.write('\n')
    f.close()


def generate_chars(train_name):
    all_names = train_name.split('-')[-3]
    char_codes = all_names.split('_')
    plate_numbers = ""
    for i in range(len(char_codes)):
        char_code = char_codes[i]
        if i == 0:
            # province
            plate_numbers  = plate_numbers + provinces[int(char_code)]
        else:
            plate_numbers = plate_numbers + char_list[int(char_code)]
    return plate_numbers
if __name__ == '__main__':
    generate_train_dataset()