
from io import StringIO

def test1(filename):
    with open(filename,'rb') as fr:

        while True:
            try:
                s = fr.readline()
                print(s.decode())
            except:
                pass


if __name__ == '__main__':
    test1("D:/fall11_urls.txt")