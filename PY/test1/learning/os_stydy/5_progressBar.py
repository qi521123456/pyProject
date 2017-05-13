import sys,time

def bar1(n):
    cursor = {0:'/',1:'|',2:'\\',3:'--'}
    for i in range(n+1):
        j = i % 4
        sys.stdout.write('\r%s%s%%' % (cursor[j],str(round(i * 100 / n, 2))))
        sys.stdout.flush()
        time.sleep(0.001)

def bar2(n):
    # sys.stdout.write('==============')
    print('='*n,end='\n')
    for i in range(n+1):
        sys.stdout.write('%s' % '#')
        sys.stdout.flush()
        time.sleep(0.5)

def bar3(n):
    for i in range(n+1):
        j = i*100//n
        sys.stdout.write('\r'+'#'*j+'='*(100-j))
        sys.stdout.flush()
        time.sleep(0.5)

bar3(100)
