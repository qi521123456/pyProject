class TestClassMethod(object):
    '''
    test1为实例方法

test2为类方法，第一个参数为类本身

test3为静态方法，可以不接收参数

类方法和静态方法皆可以访问类的静态变量(类变量)，但不能访问实例变量，test2、test3是不能访问self.name的,而test1则可以


#----------------------------------
1、类方法是属于整个类，而不属于某个对象。
2、类方法只能访问类成员变量，不能访问实例变量，而实例方法可以访问类成员变量和实例变量。
3、类方法的调用可以通过类名.类方法和对象.类方法，而实例方法只能通过对象.实例方法访问。
4、类方法只能访问类方法，而实例方法可以访问类方法和实例方法。
5、类方法不能被覆盖，实例方法可以被覆盖。

    '''


    METHOD = 'method hoho'

    def __init__(self):
        self.name = 'leon'

    def test1(self):
        print('test1')
        print(self)

    @classmethod
    def test2(cls):
        print (cls)
        print ('test2')
        print (TestClassMethod.METHOD)
        print( '----------------')

    @staticmethod
    def test3():
        print( TestClassMethod.METHOD)
        print('test3')

if __name__ == '__main__':
    a = TestClassMethod()
    a.test1()
    a.test2()
    a.test3()
    TestClassMethod.test3()
    TestClassMethod.test2()
