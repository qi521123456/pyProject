s = 'whar is jjj'
# print(s.replace(' ','%20'))
# for i in s:
#     print(i)
#
# print("pop"[-1])
# t = '1'
# print(t != '',s[-1] is '!')

print(s[:s.rfind(' ')+1],len(s))

print("i am a boy '{0}'".format(1))

# eval
sl = b"{'a':1,3:4,'r':5}"
print(eval(sl),type(sl),eval(str(sl)),s.encode("utf-8"))

print(eval('1+1'))