# coding:utf-8
'''
替换函数体，将函数体内原本字节码的位置存储数据并且解压缩执行的例子
'''
from code_obfuscate import CodeObfuscate, advanced
import marshal
import types
import zlib


def add():
    print("你好,沙雕")


t_code = '''
import zlib
import marshal
def add(a,b):
    return a+b
print "Run Func 'add' func_code"
exec (marshal.loads(zlib.decompress(add.func_code.co_code[::-1])))
'''

t_insert_code = '''
print("xdcfgvbhjnkjbhvgcf")
print("这里是测试要加密的代码")
'''
c = compile(t_code, "<string>", "exec")
c1 = compile(t_insert_code, "<string>", "exec")  # 被插入的对象，用于替换t_code中的add函数
c = CodeObfuscate(c)
for x in range(100):
    c.obfuscate(advanced)

def joinFunc(func, code):
    '''
    拼接到函数的code对象中，这里是为了字节码对象的最后一步包装
    这个函数并不能返回回去继续调用，只是为了包装code对象成为func对象的字节码，也就是存储在代码段的数据

    :param func: 传入一个函数(该函数无各种需要，code对象只是为了放在这个func对象中，func对外还是有显示的，所以开放给用户)
    :param code: 传入一个code对象，这个code对象是需要放在func的body中的code
    :return:
    '''
    # dump code对象，进行压缩，就真的可以放到代码段的位置了
    code = marshal.dumps(code)
    code = zlib.compress(code, 9)
    f = CodeObfuscate(func.func_code)
    f.co_code = code[::-1]
    code = f.get_code()
    f = types.FunctionType(code, func.func_globals, func.func_name,
                           func.func_defaults, func.func_closure)
    return f

# 拼接code对象到函数内，函数就算是可以获取到内容也无所谓，毕竟无法进行编译
f = joinFunc(add, c1)

c.co_consts[2] = f.func_code

# 看似内置有一个对象，实则是一个隐藏了内容的对象，这段内容并不放在字节码中，有可能被误解成垃圾数据丢掉
print(f.func_code)
code = c.get_code()
print("=" * 100)
exec (code)
