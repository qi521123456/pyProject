import json
import datetime
filename = "D:/cns7.json"
def get_data(filename=filename):
    with open(filename,'r') as fr:
        #data = json.loads(json.dumps(fr.read()))
        data = eval(fr.read())
        print([k for k in data['matches'][1]])
        t = data['matches'][1]['timestamp']
        print(t)
        for d in data['matches']:
            if d['data'] is not '':
                print(d['data'])


get_data()
t = "2017-03-23T22:31:51.840783"
print(t[:t.find('.')].replace('T',' '))