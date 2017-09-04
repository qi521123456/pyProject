from elasticsearch import Elasticsearch
es = Elasticsearch(["http://norn_admin:123456@192.168.120.33:9200"])
body = {"size":10,"query":{
                                    "bool":{
                                            "must":[
                                                    {"match":{"protocol_transport":"TCP"}},

                                                    {"bool":{"should":[{"match":{"port":103}},{"match":{"port":102}}]}},
                                                    {"match":{"protocol_application":"S7Comm"}}

                                            ]
                                    }
                            }
                 }
res = es.search(index="norn",doc_type="ResultProbe",body=body)
print(res)