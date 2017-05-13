import requests
ip = "183.55.116.95"
res = requests.get('http://api.map.baidu.com/location/ip?ak=32f38c9491f2da9eb61106aaab1e9739&ip='+ip+'&coor=bd09ll')
print(eval(res.content),"====")

