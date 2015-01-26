import datetime,time,struct,os,time,sys,json
from socket import *
time_server = ('time.nist.gov', 123)
TIME1970 = 2208988800L
setdefaulttimeout(5)
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
	class GMT8(datetime.tzinfo):
		def utcoffset(self, dt):
			return datetime.timedelta(hours=8) + self.dst(dt)
		def dst(self, dt):
			return datetime.timedelta(0)
		def tzname(self,dt):
			return "GMT +8"
	S = getstamp()
	T = time.time()-S
	if T<0:
		T=0
	open(os.path.split(os.path.realpath(__file__))[0]+"/time.txt","a").write(json.dumps([time.ctime(S),time.ctime(time.time()),T])+"\n")
	return [datetime.datetime.fromtimestamp(time.time(),tz=GMT8()).hour,T]
#Now()