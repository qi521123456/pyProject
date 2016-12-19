class test:
    def __init__(self):
        print("self\n")
    def __init__(self,name):
        print('name'+name)
    def __init__(self, name,age):
        print('name:%s age:%s'% (name,age))

#x=test('jobs','12')
t=test(2)
#t.hello('qqq','22')