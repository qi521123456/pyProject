import pycurl,io
import datetime

class ESAgent():
    def __init__(self, baseURL, user=None, pwd=None):
        self.agent = pycurl.Curl()
        self.agent.setopt(pycurl.URL, baseURL)
        self.url = baseURL
        if user:
            if pwd:
                self.agent.setopt(pycurl.USERPWD, str(user) + ':' + str(pwd))
            else:
                self.agent.setopt(pycurl.USERNAME, str(user))
                # self.Search('')

    def Search(self, query):
        buf = io.BytesIO()
        self.agent.setopt(pycurl.WRITEFUNCTION, buf.write)
        if query:
            self.agent.setopt(pycurl.POST, True)
            self.agent.setopt(pycurl.POSTFIELDS, query)
        else:
            self.agent.setopt(pycurl.POST, False)
        self.agent.perform()
        res = buf.getvalue().decode()
        return res

    def changeURL(self, newURL):
        self.agent.setopt(pycurl.URL, newURL)
        self.url = newURL

    def fofa2es(self, query):
        qdic = query.split()


if __name__ == "__main__":
    now = datetime.datetime.now()

    agent = ESAgent("http://192.168.205.169:9200/web_camera/web_camera/_search?pretty","elastic", "elastic")
    query = '''{
                "size": 0,
                "aggs": {
                  "country": {
                    "terms": {
                      "field": "location.country.keyword",
                      "size": 100000
                    },
                    "aggs": {
                      "province": {
                        "terms": {
                          "field": "location.region.keyword",
                          "size": 100000
                        },
                        "aggs": {
                          "city": {
                            "terms": {
                              "field": "location.city.keyword",
                              "size": 100000000
                            },
                            "aggs": {
                              "product": {
                                "terms": {
                                  "field": "protocol.keyword",
                                  "size": 1000000
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
            }'''
