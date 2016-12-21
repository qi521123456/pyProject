
def move(m,a,b,c):
    if m == 1:
        print("%s --> %s" % (a, c))
        return
    move(m-1,a,c,b)
    print("%s --> %s" % (a, c))
    move(m-1,b,a,c)


move(5, 'A', 'B', 'C')