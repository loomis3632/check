# @File  : dict_map.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/12 15:32
# @Desc  :
import re
import pickle
import chardet
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 要调取其他目录下的文件。 需要在atm这一层才可以
sys.path.append(BASE_DIR)


def get_all_path(open_file_path):
    """
    获取当前目录以及子目录下所有的.txt文件，
    :param open_file_path:
    :return:
    """
    rootdir = open_file_path
    path_list = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        com_path = os.path.join(rootdir, list[i])
        if os.path.isfile(com_path) and com_path.endswith(".txt"):
            path_list.append(com_path)
        if os.path.isdir(com_path):
            path_list.extend(get_all_path(com_path))
    return path_list


def get_encoding(file):
    """
    # 获取文件编码类型
    :param file: 文件路径
    :return: 编码
    """
    # 二进制方式读取，获取字节数据,不必全部read，检测编码类型
    with open(file, 'rb') as f:
        data = f.read(1024)
        return chardet.detect(data)['encoding']


def save_variable(v, filename):
    """
    用于保存变量
    :param v: 数据变量
    :param filename: 要保存的文件
    :return:
    """
    f = open(filename, 'wb')
    pickle.dump(v, f)
    f.close()
    return filename


def load_variable(filename):
    """
    # 读取保存的变量
    :param filename: 要读取的文件路径
    :return: 返回存储的数据
    """
    f = open(filename, 'rb')
    r = pickle.load(f)
    f.close()
    return r


def get_dict_map(stra, dict_map):
    """
    用于建立单字和序号的映射，使用字典，键：为字，值为序号
    :param stra: 字符串
    :param dict_map: 待更新的字典
    :return:
    """
    # 只保留汉字
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    stringa = "".join(pattern.findall(stra))
    # 字典长度
    dict_map_index = len(dict_map)

    for ele in stringa:
        if ele not in dict_map:  # in的速度快于haskeys（）
            dict_map[ele] = dict_map_index
            dict_map_index += 1

    return dict_map


def dict_map_train(data_dir):
    """
    按行读取大文件，建立映射
    :return:
    """
    # 要训练的数据集的文件夹

    path_lists = get_all_path(data_dir)
    count = 0
    for path in path_lists:
        coding = get_encoding(path)
        dict_map = load_variable(BASE_DIR + '/model/dict_map.txt')  # 加载已保存的映射
        with open(path, "r", encoding=coding, errors="ignore") as f:
            for ele in f:
                dict_map = get_dict_map(ele, dict_map)
                print(count)
                count += 1
        # 更新，重新保存。
        save_variable(dict_map, BASE_DIR + r'/model/dict_map.txt')
        save_variable(len(dict_map), BASE_DIR + r'/model/dict_map_length.txt')


if __name__ == '__main__':
    # rootdir = r'E:\dataset\语料\zhcrosscorpus.txt'
    rootdir = r'E:\dataset\语料'
    dict_map_train(rootdir)
