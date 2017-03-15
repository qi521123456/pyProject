import requests
from bs4 import BeautifulSoup
header = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
          'cookie':r'__cfduid=d3c474a331a92e2947c1f1ee8228090b81475030533; AJSTAT_ok_times=2;'
                   r' polito="600739f9e6da0077937c8e60fefa585058c604af57eb5a9ce449853ebf8ae5a5!";'
                   r' _LOCALE_=en; session="29981e24241882387285b8a91a6009fd880e7c63gAJVQDUwNTk1ZG'
                   r'RjZWEzMDBkZTBiMTFhNjZkM2M2Y2JlYzBjY2MwZmYzMTZiMWUzODU5YTZkNzY3YjcwMWVlOTA3YjhxAS4\075";'
                   r' _ga=GA1.2.1971536465.1475030534'}
response = requests.Session().get('https://www.shodan.io/search?query=huawei+Routing&page=2',headers=header)
print(response.text)