import datetime,time,struct,os,time,sys,json,re
from socket import *
time_server = ('time.nist.gov', 123)
TIME1970 = 2208988800L
setdefaulttimeout(5)
Tran_Month = {"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Sept":"9","Oct":"10","Nov":"11","Dec":"12"}
class GMT8(datetime.tzinfo):
	def utcoffset(self, dt):
		return datetime.timedelta(hours=8) + self.dst(dt)
	def dst(self, dt):
		return datetime.timedelta(0)
	def tzname(self,dt):
		return "GMT +8"
def getstamp():
	t = 0
	ret = 0
	while t==0 and ret <3:
		client = socket( AF_INET, SOCK_DGRAM )
		data = '\x1b' + 47 * '\0'
		client.sendto(data, time_server)
		try:
			data, address = client.recvfrom( 1024 )
		except:
			print "Get time Failed"
			ret+=1
			continue
		if data:
			t = struct.unpack( '!12I', data )[10]
			if t == 0:
				print "Time Server Error!"+time.time()
				return time.time()
			else:
				ct = time.ctime(t - TIME1970)
				return t - TIME1970
		else:
			print "Get time Failed"
			ret+=1
			continue
	return time.time()
		
def Now():
	
	S = getstamp()
	T = time.time()-S
	if T<0:
		T=0
	open(os.path.split(os.path.realpath(__file__))[0]+"/time.txt","a").write(json.dumps([time.ctime(S),time.ctime(time.time()),T])+"\n")
	return [datetime.datetime.fromtimestamp(time.time(),tz=GMT8()).hour,T]
def Tran_Weibo_Ts(SRC):    #As EST Time
	D = re.split("[: ]",SRC)
	return time.mktime(time.strptime("%s %s %s %s %s %s"%(D[-1],Tran_Month[D[1]],D[2],D[3],D[4],D[5]),"%Y %m %d %H %M %S"))