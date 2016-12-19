# coding=utf-8
import requests

'''
#, auth=('user', 'pass')
print(r.status_code)
print(r.headers)
print(r.history)
#print(r.text)

'''
#r = requests.get('http://175.188.188.180/doc/page/login.asp',stream=True)
#print(r.raw.read())
'''
filename = 'D:/test1.txt'
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(10):
        print(chunk)
        print('-----------------')
        #fd.write(chunk)
'''
#form = {'username':'admin','password':'12345'}
r = requests.get('https://segmentfault.com/user/login')
print(r)