import requests


def testIp(file):
    with open(file, 'r') as fr:
        for line in fr:
            ls = line.strip().split('\t')
            # print(ls)
            url = "http://%s" % ls[0]
            if len(ls) > 1 :
                if ls[1] == '443':
                    url = "https://%s" % ls[0]
                elif ls[1]!='80':
                    url = "http://%s:%s"%(ls[0],ls[1])

            try:
                response = requests.get(url,timeout=1)
                status = response.status_code
            except:
                status = "timeout"
            print(status)

if __name__ == '__main__':
    # testIp("/home/mannix/Desktop/ip-port")
    n = int(input())
    ls = list(map(int,input().split(' ')))
    ls.append()
    su = 0
    pre = ls[0]
    for i in ls[1:]:
        su += abs(i - pre)
        pre = i
    maxd = 0
    for i in range(1, n - 1):
        d = abs(ls[i] - ls[i - 1]) + abs(ls[i + 1] - ls[i]) - abs(ls[i + 1] - ls[i - 1])
        maxd = max(maxd, d)
    print(su - maxd)


