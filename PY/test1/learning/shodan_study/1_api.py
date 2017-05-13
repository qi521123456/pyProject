import shodan
API_KEY = ["sL3MI55FC98SfQgQBagAc4s8GJoNipQF","qTay4LRtBd9Pj85cWuB9BjIpKaPuU5p2"]
api = shodan.Shodan(API_KEY[0])
# 只能拿100条:(
result = api.search("port:102 country:'CN'",page=1)
#print(result)
with open('D:/cns7.json','w') as fw:
    fw.write(str(result))
    # for data in result['matches']:
    #     fw.write(data['ip_str']+'\n')
#"https://api.shodan.io/shodan/host/search?key={YOUR_API_KEY}&query={query}&facets={facets}"
