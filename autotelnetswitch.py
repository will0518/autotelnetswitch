# Filename: net.py
# -*- coding:utf-8 -*-  

import telnetlib
import re
import time

def do_telnet(host,username,password,commands,logfile):
	g = open(logfile,'a')
	cur=[]
	tn = telnetlib.Telnet(host)
	#tn.set_debuglevel(2) #开启调试模式	
	#tn.expect([re.compile(b"login:"),]) #用正则匹配Username
	tn.expect([re.compile(b"login:"),]) #用正则匹配Username
	tn.write(username + "\n")  #匹配成功，输入user
	tn.expect([re.compile(b"Password:"),]) #同上
	tn.write(password + "\n") #同上
	time.sleep(0.1)	
	tn.read_until("SWT-") #如果读到提示符，执行下面命令
	print '###start exec cmmand on '+host	
	for command in commands:
		cur.append(str('\n'+'----start exec '+command+' on '+host))
		tn.write(command +"\n")  #输入命令
		tn.read_until(command) #如果读到"display clock"，执行下面命令，这里的操作是在后面获取返回值的时候排除"display clock"这一行数据
		time.sleep(1) #延时以确保下调命令能读到数据
		#print tn.read_very_eager() #打印执行"display clock"的返回值
		cmd = tn.read_very_eager()
		cur.append(str(cmd))
	tn.write("exit\n") #退出
	for cur1 in cur:
		#print cur1+'--------'
		g.write(str(cur1)+'\n')
	g.close()
	#print tn.read_all() #获取全部返回值
	tn.close() #关闭连接
if __name__=='__main__':
# 配置选项
	hostlist='C:/Python27/host.txt'
	logfile='C:/Python27/telnetlog.txt'
	for host1 in open(hostlist,'r'):
		host = host1.rstrip('\n')
		#host = '192.168.1.200' # Telnet服务器IP
		username = 'admin'   # 登录用户名
		password = 'admin'  # 登录密码
		#finish = ''      # 命令提示符
#		commands = ['sys','snmp-agent community write SWT_PRIVATE']
		commands = ['save force']
		do_telnet(host, username, password,commands,logfile)

		