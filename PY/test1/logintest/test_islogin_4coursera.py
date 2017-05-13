# coding=utf-8
import requests
import random,string
signin_url = "https://accounts.coursera.org/api/v1/login"
logininfo = {"email": "limengqi057@gmail.com",
             "password": "lmq1203",
             "webrequest": "true"
             }
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")
def randomString(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
XCSRF2Cookie = 'csrf2_token_%s' % ''.join(randomString(8))
XCSRF2Token = ''.join(randomString(24))
XCSRFToken = ''.join(randomString(24))
cookie = "csrftoken=%s; %s=%s" % (XCSRFToken, XCSRF2Cookie, XCSRF2Token)
post_headers = {"User-Agent": user_agent,
                "Referer": "https://accounts.coursera.org/signin",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF2-Cookie": XCSRF2Cookie,
                "X-CSRF2-Token": XCSRF2Token,
                "X-CSRFToken": XCSRFToken,
                "Cookie": cookie
                }
coursera_session = requests.Session()
login_res = coursera_session.post(signin_url,
                                  data=logininfo,
                                  headers=post_headers,
                                  )
if login_res.status_code == 200:
    print("Login Successfully!")
    print(login_res.url)
else:
    print('222',login_res.text)