import requests
url = "http://httpbin.org/"
proxies = [{'http': 'http://121.193.143.249:80'}, {'http': 'http://118.123.245.179:3128'},{'http': 'http://118.123.245.154:3128'}, {'http': 'http://121.193.143.249:80'}]
#proxy = {'http': 'http://121.193.143.249:80'}
res = requests.get(url,proxies=proxies[3],timeout=2)
print(res.text)