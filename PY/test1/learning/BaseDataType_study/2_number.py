print((2+3)//3,(2+3)/3)

import math
'''
类型工厂函数,int()，效果：浮点数取整，如int(3.5)就返回3；数字的字符形式转换成数字，如int("35")就返回35
内置函数的round(),四舍五入，第二个参数是保留小数点后多少位，默认是0，如round(3.5)返回4.0，round(3.5,1)就返回3.5，不能取整。。。囧
math模块的floor(),取小于等于的整数,如floor(3.5)返回3.0,floor(-1.5)返回-2.0，也不能取整。。。再囧
与方法1对应的就是浮点数的类型工厂函数，float()，如float(3)返回3.0,float("3.5")返回3.5
'''
print(int(3.4))


print(3**0,2&2)