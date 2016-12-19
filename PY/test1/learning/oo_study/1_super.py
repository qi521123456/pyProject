'''
【1】Python中如果子类有自己的构造函数，不会自动调用父类的构造函数，如果需要用到父类的构造函数，则需要在子类的构造函数中显式的调用。
【2】如果子类没有自己的构造函数，则会直接从父类继承构造函数，这在单继承（一个子类只从一个父类派生）中没有任何理解上的问题。
         问题：如果是多继承的情况，一个子类从多个父类派生，而子类又没有自己的构造函数，则子类默认会继承哪个父类的构造函数。
【3】子类从多个父类派生，而子类又没有自己的构造函数时，
（1）按顺序继承，哪个父类在最前面且它又有自己的构造函数，就继承它的构造函数；
（2）如果最前面第一个父类没有构造函数，则继承第2个的构造函数，第2个没有的话，再往后找，以此类推。
'''

class Animal(object):
    """docstring for Animal"""
    def __init__(self):
        pass
    def run(self):
        print('Animal is running')
    def say(self):
        print('Animal is say something...')
class Human(object):
    def __init__(self):
        pass
    def say(self):
        print('human say ...')
class Dog(Human,Animal):
    """docstring for Dog"""
    def __init__(self):

        #super(Dog,self).__init__()
        Animal.__init__(self)
        Human.__init__(self)
        #以上两种方式相同，其他不可，一般用第二种，因为构造函数可能有输入参数这样写在多继承中便于使用
    def run(self):
        print('Dog is running')

def run_twice(animal):
    animal.run()
    animal.run()

if __name__=='__main__':
    run_twice(Dog())
    Dog().say()