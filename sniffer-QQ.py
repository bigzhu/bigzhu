#@+leo-ver=4-thin-encoding=gb2312,.
#@+node:BIGZHU.20070731151203:@thin d:/bigzhu/python/python_project/sniffer-QQ.py
#@@language python
import pcap ,struct
#@+at 
#@nonl
# qq��¼��̽��
# �ο� http://www.pythonbbs.cn/thread-2160-1-1.html
#@-at
#@@c


pack=pcap.pcap() 

pack.setfilter('udp')

key=''

for recv_time,recv_data in pack: 

   recv_len=len(recv_data)

   if recv_len == 102 and recv_data[42]== chr(02) and recv_data[101] == chr(03):

      print struct.unpack('>I',recv_data[49:53])[0]

      print '��½��'

   elif recv_len == 55:

      print struct.unpack('>I',recv_data[49:53])[0]

      print '��½��'
#@nonl
#@-node:BIGZHU.20070731151203:@thin d:/bigzhu/python/python_project/sniffer-QQ.py
#@-leo
