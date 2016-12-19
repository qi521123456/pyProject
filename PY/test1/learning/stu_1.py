# vec=[2,4,6]
# ls=['傻吊']
# ls.append([3*x for x in vec if x>3])
# print(ls)
# ls=str(ls).split(',')
# print(ls)

#*args是可变的positional arguments列表，**kwargs是可变的keyword arguments列表。
# 并且，*args必须位于**kwargs之前，因为positional arguments必须位于keyword arguments之前
def test_args(first, *args):
   print('Required argument: ', first)
   for v in args:
      print('Optional argument: ', v)

#test_args(1, 2, 3)
def test_kwargs(first, *args, **kwargs):
   print('Required argument: ', first)
   for v in args:
      print('Optional argument (*args): ', v)
   for k, v in kwargs.items():
      print('Optional argument %s (*kwargs): %s' % (k, v))

#test_kwargs(1, 2, 3, 4, k1=5, k2=6)
def test_args(first, second, third, fourth, fifth):
    print('First argument: ', first)
    print('Second argument: ', second)
    print('Third argument: ', third)
    print('Fourth argument: ', fourth)
    print('Fifth argument: ', fifth)

# Use *args
args = [1, 2, 3, 4, 5]
test_args(*args)
# results:
# First argument:  1
# Second argument:  2
# Third argument:  3
# Fourth argument:  4
# Fifth argument:  5

# Use **kwargs
kwargs = {
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5
}

test_args(**kwargs)
