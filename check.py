import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 要调取其他目录下的文件。 需要在atm这一层才可以
sys.path.append(BASE_DIR)


def check(stra):
    pass


from pypinyin import pinyin, lazy_pinyin, Style
pinyin('中心')
pinyin('中心', heteronym=True)  # 启用多音字模式
pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
pinyin('中心', style=Style.TONE2, heteronym=True)
pinyin('中心', style=Style.TONE3, heteronym=True)
lazy_pinyin('中心')  # 不考虑多音字的情况