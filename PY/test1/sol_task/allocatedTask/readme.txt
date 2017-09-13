主结点发送zmap结点文件名,TaskDir:	
	id-type-port-namaphosts-scriptname-pct.zip
	1-port-[docker1@10.8.8.87,docker4@10.6.6.6]-s7comm.zip
	若type==port: zip中只包含一个white.txt,且zip名中nmaphosts为[]
	若type==protocal:zip中包含white.txt
	
zmap结点发送到主结点tmp文件夹,TmpDir：
	id-type-port-namaphosts-scriptname-pct-ihost.zip
	type==port:已完成，备份入backup/port/ 重名名为id-ihost.zip
	type==protocal:需nmap，继续发

主结点发送到nmap结点文件,TaskDir:
	id-type-port-namaphosts-scriptname-pct.zip
	与发来的一样加入一个scriptname.nse脚本
	
nmap结点至主结点,backup/protocal/:
	id-ihost.zip
	
	
config:  
	{"id":1,"type":"protocal","port":80,"zmaphosts":"['docker1@10.2.2.2','docker2@10.2.2.2','docker1@10.5.5.5']","nmaphosts":"['docker2@10.9.9.98']","ips":"[]","ipfile":"/data/10000.txt","scriptname":"s7comm","pct":"-sU"}
	{"id":2,"type":"port","port":161,"zmaphosts":"['docker1@10.2.2.2']","nmaphosts":"[]","ips":"['202.2.2.2/24','56.6.6.6/24']","ipfile":"","scriptname":"","pct":"-sS"}