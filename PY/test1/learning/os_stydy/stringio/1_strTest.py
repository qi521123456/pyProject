import requests
from io import StringIO

def test1(filename):
    with open(filename,'rb') as fr:

        while True:

            try:
                s = fr.readline()
                # print(s.decode())
                url = s.decode()
                if url.strip() is not "":
                    url = url.strip().split()[-1]
                get_img(url)
            except:
                pass


url = "http://static.flickr.com/198/444976194_46a5b0c6a6.jpg"
def get_img(url):
    # print(url)
    name = url[url.rfind('/') + 1:url.rfind('.')]
    try:
        re = requests.get(url,timeout=1)
        print(re.status_code)
        if re.status_code != 200:
            return
        with open("D:/a/"+name+".jpg",'wb') as fw:
            fw.write(re.content)
    except:
        pass

if __name__ == '__main__':
    test1("D:/fall11_urls.txt")
    # print(url[url.rfind('/')+1:url.rfind('.')])
    # get_img(url)