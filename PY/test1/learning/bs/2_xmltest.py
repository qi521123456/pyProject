from bs4 import BeautifulSoup

fr = open("D:/161open.xml",'r')
soup = BeautifulSoup(fr,'lxml-xml')

with open("D:/161ips.txt",'w') as fw:
    for host in soup.find_all('host'):
        if host.ports.port.state.attrs['state'] == "open":
            # print(host.address.attrs['addr'])
            fw.write(host.address.attrs['addr']+'\n')
