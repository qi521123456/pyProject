import shodan

API_KEY = "sL3MI55FC98SfQgQBagAc4s8GJoNipQF"
api = shodan.Shodan(API_KEY)
# 只能拿100条:(
result = api.search('port:161')
print(result)
# with open('D:/hwips.txt','w') as fw:
#     for data in result['matches']:
#         fw.write(data['ip_str']+'\n')