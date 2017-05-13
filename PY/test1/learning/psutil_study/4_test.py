import time,psutil,socket

class NodeStatus:
    def __init__(self):
        time.sleep(0.5)
        self.nodeIP = self.get_ip()
        self.nodeDetail = {
            'cpu': str(psutil.cpu_percent())+'%',
            'tStorage': str(psutil.disk_usage("/").total/(1024*1024)) + 'M',
            'uStorage': str(psutil.disk_usage("/").used/(1024*1024)) + 'M'
        }
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('1.255.255.255', 0))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    def __str__(self):
        return "{'nodeIP':"+self.nodeIP+",'nodeDetail':"+str(self.nodeDetail)+"}"



print(str(NodeStatus()).encode('utf-8'))