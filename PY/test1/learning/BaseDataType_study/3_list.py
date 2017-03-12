l = [3,4,5,6,7,'er',8]
def t1():
    print(l[:-1],l[2:])
    l2=[[3,4,5,6,7],[8,9,10,34,5],[]]
    subl2=[]
    for i in l2:
        subl2.append(i[1:])
    print(subl2)

    print(i[1:])

    l3 = {1,2,3,4,5,6,7,8}
    for i in l3:
        pass
        #print(i)
    l.extend(['ss',9])
    print(l)
    l.append('cc')
    print(id(l))
    print(l.pop(5))
    #print(min(l2[2]),l)
    print(not 'er' in l)

    print(l+[3,2])

for i in l:
    print(i)

