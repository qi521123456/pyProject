# coding utf-8
import pymongo
#链接mongodb
client=pymongo.MongoClient(host="127.0.0.1",port=27017)
#db=client.SOL
#coll=db.ipChina
coll=client['SOL']['ipChina']
#print("hello"+str(coll.find_one())+"\n"+str(coll.count()))

while True:
    oneIp=int(input("请输入ip： "))
    locs=coll.find({"end_ip":{"$gte":oneIp},"start_ip":{"$lte":oneIp}},{"_id":0,"location":1})
    if locs.count()!=0:
        for item in locs:
            print(item['location'])
    else:
        print("找不到！")
     #input("按enter退出")

#print(coll.find_one({"end_ip":{'$gte':2000000}}))
