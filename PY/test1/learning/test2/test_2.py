def ch1(num):
    s = []
    for i in range(4):
        s.append(str(int(num % 256)))
        num /= 256
        print(i)
    print(s)
    return '-'.join(s[::-1])
print(ch1(123456789))
"""
#s[::-1]#翻转
#s[::2]#隔一个取一个

ls=['a','b',1,3,('a','s')]
#ls[-1:0]=['hello']
#print(len(ls))
#num_inc_list=range(30)
slist=[0]*5
#print(slist)
print(ls[3:])

var=""
index=0
L = range(1,5)      #即 L=[1,2,3,4],不含最后一个元素
L = range(1, 10, 2) #即 L=[1, 3, 5, 7, 9]
L.append(var)   #追加元素
L.insert(index,var)
L.pop(var)      #返回最后一个元素，并从list中删除之
L.remove(var)   #删除第一次出现的该元素
L.count(var)    #该元素在列表中出现的个数
L.index(var)    #该元素的位置,无则抛异常
L.extend(ls)  #追加list，即合并list到L上
L.sort()        #排序
L.reverse()     #倒序

a[1:]       #片段操作符，用于子list的提取
[1,2]+[3,4] #为[1,2,3,4]。同extend()
[2]*4       #为[2,2,2,2]
del L[1]    #删除指定下标的元素
del L[1:3]  #删除指定下标范围的元素

L1 = L      #L1为L的别名，用C来说就是指针地址相同，对L1操作即对L操作。函数参数就是这样传递的
L1 = L[:]   #L1为L的克隆，即另一个拷贝。

a = [3, 3, 5, 7, 7, 5, 4, 2]
a = list(set(a)) # [2, 3, 4, 5, 7] 连排序都做好了
"""