# coding:uft-8
'''
一个闭包就是你调用了一个函数A，这个函数A返回了一个函数B给你。这个返回的函数B就叫做闭包。你在调用函数A的时候传递的参数就是自由变量。
'''
def line_conf(a, b):
    def line(x):
        return int(str(a)+str(x)) + b

    return line


line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))