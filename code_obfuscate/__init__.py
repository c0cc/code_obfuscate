# coding:utf-8
'''
这里面的函数都是混稀器
'''
from opcode import HAVE_ARGUMENT
from .obfuscate import PycFileObfuscate, PyFileObfuscate, CodeObfuscate
from .utils import sum_jump, generate_line
import random


def overlapping_Instruction(index):
    '''
    重叠字节码混淆，⚠️，这个混淆只可以用一次，就是在最后一次混淆，因为字节码重叠了
    程序计算的时候会出现问题，最后就会导致文件失效

    请勿觉得自己很屌或者随便运行一下觉得没问题就行了，这个是真的会乱，跳转算不出来

    每使用一次该混淆器，字节码会增加9或12字节码
    :param index: 上层通知混淆的位置，就是当前要放置的位置，返回的payload会自动计算
    :return:
    '''

    # 混淆内容的关键位置
    change = (
        "\x71\x04\x00" +  # jump 04
        "\x64\x71\x07" +  # LOAD_CONST 1905
        "\x00",  # -- -- stop code
        "\x64", "??,??",  # code
    )
    ret = "\x71%s" % sum_jump(index + 4)  # 一次跳转
    two_jump = sum_jump(index + 9)  # 二次跳转
    if ord(two_jump[-1]) >= HAVE_ARGUMENT:  # 如果跳的有点远，需要重新计算
        two_jump = sum_jump(index + 12)
        two_jump += "\xff\xff\x00"
    ret += "\x64\x71%s\x64\xff" % two_jump
    return ret


def ordinary(index):
    '''
    一个可以多次使用并且工作状态良好的混淆器，这个混淆器一般没什么问题，只是有一条绝对跳转加上一条混淆指令

    每使用一次该混淆器，字节码会增大6字节的长度，也就是两条指令

    :param index: 上层通知混淆的位置，就是当前要放置的位置，返回的payload会自动计算
    :return:
    '''

    def g_line():
        return chr(random.randint(0, 255)) + chr(random.randint(0, 255))

    obfs_codes = [
        "\x71%s\x64%s" % (sum_jump(index + 6), g_line()),  # JUMP_ABSOLUTE 6,LOAD_CONST rand
        "\x71%s\x62%s" % (sum_jump(index + 6), g_line()),  # JUMP_ABSOLUTE 6,DELETE_GLOBAL rand
        "\x71%s\x74%s" % (sum_jump(index + 6), g_line()),  # JUMP_ABSOLUTE 6,LOAD_GLOBAL rand
        "\x71%s\x5b%s" % (sum_jump(index + 6), g_line()),  # JUMP_ABSOLUTE 6,DELETE_NAME rand
    ]
    return random.choice(obfs_codes)


def insert_Identification(msg, index):
    '''
    插入标识,该标识主要是有一个长的字符串构成
    字符串本身有一部分可以解释成opcode
    有一部分不能解释成opcode的会对解析造成困难

    警告⚠️: 这个混淆部分推荐是只插入一次，插入多了怕插进去的信息出问题
    每使用一次该混淆器，字节码会增加信息长度加3字节码
    该函数目前测试如果纯汉字加数字等于号，换行，多次混淆不会出问题，但是加入字母就经常出问题了

    :param index: 上层程序传入给这个函数的参数，其值为将要将这个数据插入的位置，计算好自己要插入的数据跳转的位置
    :return:
    '''

    r = "\x71%s%s" % (sum_jump(index + len(msg) + 3), msg)
    return r


def advanced(index):
    '''
    这个混淆器会先获取随机数，根据随机数获取行的数量，然后放到一起

    每使用一次该混淆器，字节码会增加信息长度加随机数三倍加3字节码

    :param index:
    :return:
    '''

    count = random.randint(1, 20)
    codes = ""
    for _ in range(count):
        codes += generate_line()
    return "\x71%s%s" % (sum_jump(index + 3 + len(codes)), codes)
