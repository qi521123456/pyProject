# 导入 socket、sys 模块
import socket
import sys,threading,time

# 创建 socket 对象
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
# host = socket.gethostname()

port = 9999
def tcplink(sock, addr):
    print('Accept new connection from %s...%s' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)
# 绑定端口
s.bind(('127.0.0.1', port))

# 设置最大连接数，超过后排队
s.listen(5)
print('Waiting for connection...')
# while True:
#     # 建立客户端连接
#     clientsocket, addr = serversocket.accept()
#
#     print("连接地址: %s" % str(addr))
#
#     msg = '欢迎访问菜鸟教程！' + "\r\n"
#     clientsocket.send(msg.encode('utf-8'))
#     print(clientsocket.recv(1024).decode())
#     clientsocket.send(clientsocket.recv(1024)+',too'.encode())
#     clientsocket.close()
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
