# coding:utf-8
'''
简单的对py文件混淆的输出，py文件实际上的过程是会被编译成pyc文件，然后读字节码
'''
from code_obfuscate import PyFileObfuscate, advanced, insert_Identification
from functools import partial

pyf_obfu = PyFileObfuscate("/Users/minisys/PycharmProjects/scan_core/lscore/obfus/tmp.py")
for line in range(200):
    pyf_obfu.obfuscate(advanced)
for line in range(100):
    pyf_obfu.obfuscate(partial(insert_Identification,
                               "\r\n\r\n=======================================\r\n\r\n测试的字符串\r\n\r\n=======================================\r\n\r\n"))
for x in range(100):
    pyf_obfu.obfuscate(partial(insert_Identification, "望咩啊，死仔"))

pyf_obfu.change_all_filename("望咩啊，死仔") # 这里会暴露编译的位置，该方法会同时递归处理常量中的文件名信息
pyf_obfu.write("/Users/minisys/tmp.pyc")
