try:
    #from utils.logging import Logging
    import requests
    import json
except Exception as e:
    print(e)


class Shodan:

    def __init__(self):
        self.key = "hVyYutxJAUp0gyfbdlqay6Luh6n6smGI"
        self.url = "https://api.shodan.io"
        #self.logger = Logging().get_logger()

    def search_by_port(self,port,country="CN"):
        url = self.__get_url("shodan","host","search")
        query = "port:%s country:%s" % (str(port),country)

        params = {"key":self.key,"query":query}
        query_res = list()

        try:
            response = json.loads(requests.get(url,params).text)
            matches = response.get('matches')
            for matche in matches:
                query_res.append(matche.get('ip_str'))
        except Exception as e:
            print(e)
        finally:
            return query_res

    def search_by_product(self,key,**kwargs):
        url = self.__get_url("shodan","host","search")
        query = key
        for k in kwargs:
            query += " %s:%s" % (k,kwargs.get(k))

        params = {"key":self.key,"query":query}
        query_res = list()

        try:
            response = json.loads(requests.get(url,params).text)
            matches = response.get('matches')
            for matche in matches:
                query_res.append(matche.get('ip_str'))
        except Exception as e:
            print(e)
        finally:
            return query_res

    def __get_url(self,*args):
        url = self.url
        for arg in args:
            url+="/%s" % arg
        return url


if __name__ == '__main__':
    res = Shodan().search_by_port('44818')
    print(res)
