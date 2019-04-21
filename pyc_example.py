# coding:utf-8
'''
简单的读取pyc文件，并且进行混淆
'''
from code_obfuscate import PycFileObfuscate, advanced, insert_Identification
from functools import partial

pyf_obfu = PycFileObfuscate("/Users/minisys/PycharmProjects/scan_core/lscore/obfus/tmp.pyc")
for line in range(200):
    pyf_obfu.obfuscate(advanced)
for line in range(100):
    pyf_obfu.obfuscate(partial(insert_Identification,
                               "\r\n\r\n=======================================\r\n\r\n这里不知道是什么东西\r\n\r\n=======================================\r\n\r\n"))
for x in range(100):
    pyf_obfu.obfuscate(partial(insert_Identification, "看个鸡儿"))

pyf_obfu.change_all_filename("望咩啊，死仔")
pyf_obfu.write("/Users/minisys/tmp.pyc")
