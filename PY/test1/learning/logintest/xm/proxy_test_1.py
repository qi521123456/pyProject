import requests
url = "http://httpbin.org/"
proxies = [{'http': 'http://121.193.143.249:80'}, {'http': 'http://111.155.116.240:8123'}, {'http': 'http://180.175.145.148:808'}, {'http': 'http://139.208.86.204:80'},{'http': 'http://118.123.245.154:3128'}, {'http': 'http://121.193.143.249:80'}]
#proxy = {'http': 'http://121.193.143.249:80'}
res = requests.get(url,proxies=proxies[1],timeout=2)
print(res.status_code,res.text)