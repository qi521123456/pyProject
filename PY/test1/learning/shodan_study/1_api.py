import shodan
API_KEY = "sL3MI55FC98SfQgQBagAc4s8GJoNipQF"
api = shodan.Shodan(API_KEY)
# 只能拿100条:(
result = api.search('cisco rout')
#print(result)
with open('D:/hwRips.txt','w') as fw:
    for data in result['matches']:
        fw.write(data['ip_str']+'\n')
#"https://api.shodan.io/shodan/host/search?key={YOUR_API_KEY}&query={query}&facets={facets}"
