# encoding=utf-8
import requests

if __name__ == "__main__":
    phonenum = '18810398057'
    pwd = 'lmq1203'
    mainURL = 'http://220.134.160.87/doc/page/main.asp'
    loginURL = 'http://220.134.160.87/doc/page/login.asp'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}

    s = requests.session()
    r = s.get(mainURL)
    print(r.cookies)  # 打印页面cookies，可在终端自己查看

    login_data = {'phone_num': phonenum, 'password': pwd}
    t = s.post(loginURL, login_data, headers)
    print(t.text)  # 显示登录结果，正常情况下应该是{"r:"0,"msg":"\u767b\u9646\u6210\u529f"}，"msg"字段中显示的是登录结果(Unicode)

    t = s.get(mainURL)
    print(t.status_code)
    #print(t.text.encode('utf-8'))
