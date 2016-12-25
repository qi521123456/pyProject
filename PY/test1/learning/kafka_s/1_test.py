from kafka import KafkaProducer

# class tostr():
#     def __init__(self, task_id, task_strategy, port, ip_src, script_data=None, scan_pro='-sS'):

d = {'task_id': 1223, 'task_strategy': True, 'port': 80, 'ip_src': [], 'script_data': None, 'scan_pro': '-sS'}
print(type(eval(str(d))))
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send('test', str(d).encode("utf-8"))