import socket
import psutil
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        mac = ''
        ip = s.getsockname()
        for k, v in psutil.net_if_addrs().items():
            print(k)
            if k == 'docker0':
                for item in v:
                    address = item[1]
                    if len(address) == 17:
                        mac = address
                        break
    finally:
        s.close()

    return ip,mac

if __name__ == '__main__':
    print(get_host_ip())

