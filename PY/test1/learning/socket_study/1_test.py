import socket,struct
sip = '127.0.0.1'
print(socket.inet_aton(sip),struct.unpack("I", socket.inet_aton(sip)))
print(socket.ntohl(1677222))

print(socket.gethostname())