import requests
import base64
KEY = "5d18dd2308793e56b2ff0bd22dd59a36"
email = "651701497@qq.com"
q = "port=80"
bq = base64.b64encode(q.encode()).decode()

#url = "https://fofa.so/api/v1/search/all?email=%s&key=%s&qbase64=%s" % (email,KEY,bq)

header = {
    'Cookie':'AJSTAT_ok_times=1; locale=zh-CN; _fofapro_ars_session=2d037f5f15cb971a83f5771738406cea'
}
url = "https://fofa.so/result?page=3&qbase64=cG9ydD04MA%3D%3D"
result = requests.get(url,headers=header)
print(result.text)