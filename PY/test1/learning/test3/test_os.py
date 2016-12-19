import os
#print(os.environ)


print(os.path.abspath('.'))
for x in os.listdir('..'):
    if os.path.isdir(os.path.join('..', x)):
        print(x)