
def puciz(n):
    a1 = 1
    a2=1
    a3=2
    for i in range(4,n+1):
        tmp = a3
        a3 = a1+a3
        a1 = a2
        a2 = tmp

        print(i,a3)

if __name__ == '__main__':
    puciz(20)