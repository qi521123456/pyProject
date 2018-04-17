import json
from elasticsearch5 import Elasticsearch
import datetime


if __name__ == "__main__":
    now = datetime.datetime.now()
    es = Elasticsearch(hosts=['192.168.205.169:8200'],http_auth=('elastic','elastic'))

    # agent = ESAgent("http://192.168.205.169:9200/web_camera/web_camera/_search?pretty","elastic", "elastic")
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
    a = es.search(index='web_camera',doc_type='web_camera',body=query)
    print(a)