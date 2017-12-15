import requests
def getData(path):
    data = {}
    with open(path,'r') as fr:
        for line in fr:
            l = line.split(',')
            data[l[-1]] = 0




if __name__ == '__main__':
    q = requests.delete("http://localhost:9200/weather")
    print(q)