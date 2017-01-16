from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from pymongo import MongoClient
from functools import reduce

class MongoDBInterface:
    """mongodb API whitch capsulation methods called by other such DslComplier """

    def __init__(self):
        self.db_client = None
        self.db_conn = None
        self.prefix = "mongodb://"

    def connect(self,ip,database_name,username,password):
        """Method for connect mongodb

        :Parameters:
          - 'ip' : ip address of mongodb
          - 'database_name' : database for connect
          - 'username' : valid username of authenticate mongodb
          - 'password' : valid passsword if authenticate mongodb

        :Returns:
          True if connect success else False
        """
        return self.__open(ip,database_name,username,password)

    def delete(self,fields=None,collection=None,condition=None):
        if collection is None:
            return False
        condition = {} if condition is None else condition
        db_collection = self.db_conn[collection]
        try:
            #fields is None means delete existing document else update
            if fields is None:
                del_result = db_collection.delete_many(condition)
                del_status = del_result.raw_result['ok']
                return True if del_status is 1 else False
            else:
                fields = fields.split(',')
                del_fields = dict()
                for i in fields:
                    del_fields[i] = ""
                del_fields = {"$unset": del_fields}
                del_result = db_collection.update_many(condition,del_fields)
                del_status = del_result.raw_result['ok']
                return True if del_status is 1 else False
        except:
            return False
    def query(self,fields,collection,condition):
        """Query the document form collection by specific condition

        :Parameters:
          - 'fields' : fields which need query and each other split by ','
          - 'collection' : the collection which need to query
          - 'condition' : query condition for filter document

        :Returns:
          list if query success else None
        """
        try:
            collections = collection.split(',')
            temp_list = list()
            for item in collections:
                temp_list.append(self.__single_query(fields,item,condition))
            res_list = reduce(lambda x, y: x+y, temp_list)
            return res_list
        except:
            return None

    def insert(self,fields_and_valus,collection,condition):
        """Insert document by condition into collection

        :Parameters:
          - 'fields_and_valus' : key-value data which need to insert
          - 'collection' : target collection to insert document
          - 'condition' : filter for insert,insert if none else update

        :Returns:
          True if insert success else False
        """
        if collection is None or fields_and_valus is None:
            return False
        try:
            db_collection = self.db_conn[collection]
            if condition is None:
                #condition is None means to insert new document
                inser_res = db_collection.insert_one(fields_and_valus)
                return inser_res.acknowledged
            else:
                #condition is not none means update existing document
                key = list(fields_and_valus.keys())[0]
                if isinstance(fields_and_valus.get(key),dict):
                    up_doc = {"$push":fields_and_valus}
                else:
                    up_doc = {"$set": fields_and_valus}
                up_res = db_collection.update_one(condition,up_doc)
                if up_res.raw_result['nModified'] > 0:
                    return True
                else:
                    return False
        except:
            return False

    def __open(self,ip,database_name,username,password):
        if(database_name is None) or (username is None) or (password is None):
            return False
        if ip is None:
            ip = "127.0.0.1:27017"
        try:
            ip = self.prefix + ip
            self.db_client = MongoClient(ip)
            self.db_conn = self.db_client[database_name]
            db_collection = self.db_conn["User"]
            data = dict()
            data["name"] = username
            data["password"] = password
            res = db_collection.find_one(data)
            return False if res is None else True
        except:
            self.db_conn = None
            return False

    def __open_2(self,ip,database_name,username,password):
        if(database_name is None) or (username is None) or (password is None):
            return False

        if ip is None:
            ip = "127.0.0.1:27017"

        try:
            ip = self.prefix + ip
            self.db_client = MongoClient(ip)
            self.db_conn = self.db_client[database_name]
            return self.db_conn.authenticate(username,password)
        except Exception:
            return False
        except Exception:
            return False

    def __close(self):
        try:
            self.db_client.close()
            self.db_client, self.db_conn = None, None
            return True
        except:
            return False

    def __single_query(self,fields,collection,condition):
        if collection is None:
            return None
        try:
            db_collection = self.db_conn[collection]
            query_res = list()
            if fields is None:
                #case condition is None or not
                find_res = None
                if condition is None:
                    find_res = db_collection.find()
                else:
                    find_res = db_collection.find(condition)
                for item in find_res:
                    query_res.append(item)
                return query_res
            else:
                find_fields = dict()
                for i in fields.split(','):
                    find_fields[i] = 1
                #case condition is None or not
                if condition is None:
                    find_res = db_collection.find(None,find_fields)
                else:
                    find_res = db_collection.find(condition,find_fields)
                for item in find_res:
                    query_res.append(item)
                return query_res
        except:
            return None

    def __merge_list(self,left_list,right_list):
        """Merge two list and retain common item

        :Paramters:
          - 'left_list' : one list for merge
          - 'right_list' : one list for merge

        :Returns:
          new list by merge left_list and rigth_list
        """
        return [val for val in left_list if val in right_list]

    def del_for_results(self,condition):
        fields = "history.record.native.results"
        collection = "Project"
        try:
            find_res = self.query(fields,collection,None)
            for item in find_res:
                index_h,index_n = self.__get_index(condition,item)
                if index_h != -1 and index_n != -1:
                    command = "history.%s.record.native.%s.results" % (index_h,index_n)
                    command = {"$pull":{command:condition}}
                    db_collection = self.db_conn[collection]
                    p_id = item.get('_id')
                    from bson.objectid import  ObjectId
                    p_id = ObjectId(p_id)
                    condition = {"_id": p_id}
                    up_res = db_collection.update_one(condition,command)
                    if up_res.raw_result['nModified'] > 0:
                        return True
                    else:
                        return False
            return False
        except Exception as e:
            return False

    def __get_index(self,condition,data):
        try:
            history = data.get('history')
            for h_index in range(len(history)):
                native = history[h_index].get('record').get('native')
                for n_index in range(len(native)):
                    results = native[n_index].get('results')
                    for item in results:
                        if item.get('id') == condition.get('id'):
                            return h_index,n_index
            return -1,-1
        except Exception as e:
            return -1,-1


def get_ip_range(start_ip,end_ip):
    if start_ip == end_ip:
        return start_ip
    s_ips = start_ip.split('.')
    e_ips = end_ip.split('.')
    for i in range(len(s_ips)):
        if s_ips[i] != e_ips[i]:
            result = start_ip + "/%s" % str(i * 8)
            return result


#-----------------------------------------------------------------------
def test():
    mi = MongoDBInterface()
    mi.connect('127.0.0.1','SOL','admin','Free-Wi11')
    i = 1
    while i<=1:
        if i is 1:
            url = r"http://ip.yqie.com/cn/shandong/weihai/"
        else:
            url = r"http://ip.yqie.com/search.aspx?pagecurrent=%s" % str(i)
            url += "&searchword=%E6%96%B0%E7%96%86"
        print(url)
        html = urlopen(url).read()
        html = BeautifulSoup(html)
        table = html.find('table',id='GridViewOrder')
        trs = table.find_all('tr')
        for index in range(len(trs)):
            if index > 0:
                tds = trs[index].find_all('td')
                item = {}
                for j in range(len(tds)):
                    if j is 0:
                        pass

                    elif j is 1:
                        item['start_ip'] = tds[j].text
                    elif j is 2:
                        item['end_ip'] = tds[j].text
                    else:
                        item['location'] = tds[j].text
                mi.insert(item,'IPS_WeiHai',None)
        i+=1
        time.sleep(1)
        print(i)

#甘肃,宁夏
if __name__ == '__main__':

    mi = MongoDBInterface()
    mi.connect('localhost','SOL','admin','admin')
    res = mi.query(None,'IPS_WeiHai',None)
    for item in res:
        print(get_ip_range(item.get('start_ip'),item.get('end_ip')))