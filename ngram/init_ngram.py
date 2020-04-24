# @File  : dict_map.py
# @Author: xiangcaijiaozi
# @Date  : 2020/3/12 15:32
# @Desc  :
import re
import pickle
import collections
import numpy as np

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


def get_dict_map():
    """
    用于建立单字和序号的映射，使用字典，键：为字，值为序号
    :param stra: 字符串
    :param dict_map: 待更新的字典
    :return:
    """
    stra = "天津北京天津"
    dict_map = collections.defaultdict(int)
    #只保留汉字
    pattern = re.compile(r'[\u4e00-\u9fa5]')      # 中文的编码范围是：\u4e00到\u9fa5
    stringa = "".join(pattern.findall(stra))
    #字典长度
    dict_map_index = len(dict_map)

    for ele in stringa:
        if ele not in dict_map:  # in的速度快于haskeys（）
            dict_map[ele] = dict_map_index
            dict_map_index += 1
    save_variable(dict_map, r'./model/dict_map.txt')
    save_variable(len(dict_map), r'./model/dict_map_length.txt')
    return dict_map


# 模型建立
def count_2gram():
    stra = "天津北京天津"
    dict_map = load_variable('./model/dict_map.txt')
    # 字符串处理，只保留汉字
    pattern = re.compile(r'[\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    stringa = "".join(pattern.findall(stra))
        # numpy建立并初始化新的二维矩阵,此时的长度为新的dict_map的长度。
    matrix = np.zeros((5, 5), dtype=np.int)

    # 把输入的字符串的字符统计更新到矩阵中
    for i in range(len(stringa)):
        i += 1
        if i == len(stringa):
            break
        # print(i)
        x = dict_map.get(stringa[i - 1])
        y = dict_map.get(stringa[i])
        if x != None and y != None:  # 为了防止查询不存在的字映射
            matrix[x][y] = matrix[x][y] + 1

    save_variable(matrix, r'./model/matrix.txt')
    return matrix


if __name__ == '__main__':
    # get_dict_map()
    count_2gram()
