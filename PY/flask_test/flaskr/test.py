#coding=utf-8
from operator import itemgetter
#类定义
class people:
    #定义基本属性
    _score=0

    #定义构造方法
    def myinit(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age),self.__weight)
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self,value):
        self._score = value

# 实例化类
p = people()
p.myinit('qiqi',18,210)
p.speak()
print(p.age,p.name,p._score)

p.score=100
print(p.score)


students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

print(sorted(students, key=itemgetter(0)))
print(sorted(students, key=lambda t: t[1]))
print(sorted(students, key=itemgetter(1), reverse=True))