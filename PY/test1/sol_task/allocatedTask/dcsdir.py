import os
def createdir(dockername):
    pHead = "/home/lmqdcs/"
    pEnd = "/task/recv/"
    os.makedirs(pHead+dockername+pEnd)

if __name__ == '__main__':
    for i in range(1,5):
        createdir("docker"+str(i))