# coding utf-8
'''所有参数（变量）都是按引用传递'''
def changeme(mylist):
    "修改传入的列表"
    mylist.append([1, 2, 3, 4]);
    print("函数内取值: ", mylist)
    return
# 调用changeme函数
mylist = [10, 20, 30];
changeme(mylist);
print("函数外取值: ", mylist)


def printme(str):
    "打印任何传入的字符串"
    print(str);
    return;
# 调用printme函数
printme(str="菜鸟教程");

def printinfo(arg1, *vartuple):
    "打印任何传入的参数"
    print("输出: ")
    print(arg1)#输出第一个
    for var in vartuple:
        print(var)
    return;
# 调用printinfo 函数
printinfo(10);
printinfo(70, 60, 50);

# 匿名函数lambda
sum = lambda arg1, arg2: arg1 + arg2;
# 调用sum函数
print("相加后的值为 : ", sum(10, 20))
print("相加后的值为 : ", sum(20, 20))
