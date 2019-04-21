# code_obfuscate

python字节码简单混淆类

## 工作原理
> 对python字节码`co_code`属性内容进行垃圾数据的插入

## 使用方式

    from code_obfuscate import PycFileObfuscate, advanced, insert_Identification
    
    c = PycFileObfuscate("xxx.pyc") # 打开一个pyc文件
    for line in range(200): # 使用 advanced 混淆器，插入垃圾指令200次
        pyf_obfu.obfuscate(advanced)
    
    # 在字节码中贴上自己的版权信息，通过cat xxx.pyc可以看到
    pyf_obfu.obfuscate(partial(insert_Identification, "\r\n\r\n=======================================\r\n\r\n这里不知道是什么东西\r\n\r\n=======================================\r\n\r\n"))
    pyf_obfu.change_all_filename("望咩啊，死仔") # 更改所有code对象的文件名，方式信息的泄漏
    pyf_obfu.write("aaa.pyc") # 输出到其他文件

上面的例子导入的是 `PycFileObfuscate` 是对pyc文件混淆的类，同时还有 `PyFileObfuscate` 是对py文件编译后混淆的类(如果没有编译,会自动调用编译),以及 `CodeObfuscate` ,就是对字节码混淆的类

## 混淆函数

这个东西我习惯叫混淆器，感觉上逼格高一点

就是在 `code_obfuscate/__init__.py` 中的几个负责产生垃圾指令的函数

分别是

    overlapping_Instruction
    ordinary
    insert_Identification
    advanced

这四个函数除了 `insert_Identification`的参数是两个，其余的参数都是1个，`pyf_obfu.obfuscate`在调用的时候，传入一个生成垃圾代码的混淆器

`pyf_obfu.obfuscate`会调用这个传入的函数，然后分割指令集，找到合适的位置，把这个位置给传入的函数，就是上面这四个函数，当然也可以自己写，然后返回一段字节码，返回的字节码会进行计算，并且修正调用的位置

因为`insert_Identification` 函数比较特殊，需要传入你想要插进去的信息，所以可以使用如下的操作方式

    from functools import partial
    insert_Identification = partial(insert_Identification,"你要插入的信息")

`partial` 可以给函数添加默认参数，上面这个例子就是会给`insert_Identification` 的第一个参数设置参数为`"你要插入的信息"` 如果对上面包装后的 `insert_Identification` 进行调用，只能传入一个参数，就是第二个参数的index

下面详细介绍一下这四个函数

### overlapping_Instruction

重叠字节码混淆，这个混淆只可以用一次，就是在最后一次混淆，因为字节码重叠了

程序计算的时候会出现问题，最后就会导致文件失效

每使用一次该混淆器，字节码会增加9或12字节码

参数:`index` 整数 上层通知混淆的位置，就是当前要放置的位置，返回的payload会自动计算

返回:产生的字节码，上层会自动计算

### ordinary
一个可以多次使用并且工作状态良好的混淆器，这个混淆器一般没什么问题，只是有一条绝对跳转加上一条混淆指令

每使用一次该混淆器，字节码会增大6字节的长度，也就是两条指令

参数:`index` 整数 上层通知混淆的位置，就是当前要放置的位置，返回的payload会自动计算

返回:产生的字节码，上层会自动计算

### insert_Identification

插入标识,该标识主要是有一个长的字符串构成(该函数主要是为了什么版权信息加进去的，就是对字节码进行`cat`的时候看得到的一段信息)


警告: 这个混淆部分推荐是只插入一次，插入多了怕插进去的信息出问题

每使用一次该混淆器，字节码会增加`信息长度`加3字节码

该函数目前测试如果`汉字`加`数字` `等于号`，`换行`，多次混淆不会出问题，但是加入字母推荐只使用一次，加入字母容易计算错误

参数:`msg` 文本 需要插入到字节码中的信息

参数:`index` 整数 上层程序传入给这个函数的参数，其值为将要将这个数据插入的位置，计算好自己要插入的数据跳转的位置

返回:产生的字节码，上层会自动计算

### advanced
这个混淆器会先获取`1-20`的随机数，根据随机数获取行的数量，然后放到一起

每使用一次该混淆器，字节码会增加信息长度加随机数三倍加3字节码

参数:`index` 整数 上层程序传入给这个函数的参数，其值为将要将这个数据插入的位置，计算好自己要插入的数据跳转的位置

返回:产生的字节码，上层会自动计算
