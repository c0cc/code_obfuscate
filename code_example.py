# coding:utf-8
'''
将函数的code对象插入混淆指令，然后执行，其实可以再塞回到函数内的
'''
from code_obfuscate import CodeObfuscate, advanced, insert_Identification
import time
import dis
import sys


def hello():
    for x in range(10):
        for y in range(10):
            for z in range(10):
                print(x + y + z)
                if x + y + z == 10:
                    continue


dis.dis(hello.func_code)
import time

time.sleep(0.2)

pycode_obfu = CodeObfuscate(hello.func_code)  # 取函数的code部分，进行混淆
for line in range(200):
    pycode_obfu.obfuscate(advanced)
code = pycode_obfu.get_code()
print(code)
try:
    dis.dis(code)
except:
    time.sleep(0.2)
    sys.stderr.write("\r\n解析字节码出现问题\r\n")
time.sleep(0.2)
exec (code)