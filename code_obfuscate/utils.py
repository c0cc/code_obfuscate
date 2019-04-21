# coding:utf-8
import struct
import random


def sum_jump(index):
    '''
    计算长度，返回的内容可以写在pyc关于长度的位置
    :param length: 计算的长度
    :return: 返回长度字节
    '''
    return struct.pack("<I", index)[:2]


def generate_line():
    '''
    随机生成一个条有参数的指令
    opcpde>90 即为有参数
    :return:
    '''
    return chr(random.randint(90, 255)) + chr(random.randint(0, 255)) + chr(random.randint(0, 255))
