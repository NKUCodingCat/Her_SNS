#!/usr/bin/python
# -*- coding: utf-8 -*-
#from weibopy.api import API
from weibo import APIClient
import re, sys,os,urllib,urllib2,cookielib,httplib,time,datetime,json,t2,eml
import webbrowser
import urlparse
Self = 自己的id
Target = 妹子的id
#模拟授权并且获取回调地址上的code，以获得acces token和token过期的UNIX时间
APP_KEY = # app key
APP_SECRET = # app secret
#回调地址，可以用这个默认地址
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html' 
def get_code(): 

	AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
	USERID =  #微博账号
	PASSWD =  #微博密码
	
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	referer_url = client.get_authorize_url()
	print "referer url is : %s" % referer_url
	
	cookies = urllib2.HTTPCookieProcessor()
	opener = urllib2.build_opener(cookies)
	urllib2.install_opener(opener)
	
	postdata = {"client_id": APP_KEY,
	"redirect_uri": CALLBACK_URL,
	"userId": USERID,
	"passwd": PASSWD,
	"isLoginSina": "0",
	"action": "submit",
	"response_type": "code",
	}
	
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
	"Host": "api.weibo.com",
	"Referer": referer_url
	}
	
	req = urllib2.Request(
	url = AUTH_URL,
	data = urllib.urlencode(postdata),
	headers = headers
	)
	try:
		resp = urllib2.urlopen(req)
		print "callback url is : %s" % resp.geturl()
		code = resp.geturl()[-32:]
		print "code is : %s" % resp.geturl()[-32:]
	except Exception, e:
		print e
	return code

def begin():

	
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	
	code = get_code()
	
	r = client.request_access_token(code)
	print r
	access_token = r.access_token # 新浪返回的token，类似abc123xyz456
	expires_in = r.expires_in # token过期的UNIX时间
	
	client.set_access_token(access_token, expires_in)
	
	#发普通微博
	data = t2.Now()
	num = u"咚~"*(data[0]%12)
	if num == "":
		num = u"咚~"*12
	time.sleep(data[1])
	#client.statuses.update.post(status=num)
	#私人需求
	head = {"Authorization":"OAuth2 "+access_token}
	DB = os.listdir(os.path.split(os.path.realpath(__file__))[0]+"/DB")
	Need = GetPage(head,Self,Target)
	for j in Need:
		if str(j[0])+".json" not in DB:
			Data = json.dumps(j[1])
			f = open(os.path.split(os.path.realpath(__file__))[0]+"/DB/"+str(j[0])+".json","w")
			f.write(Data)
			f.close()
			try:
				for i in json.loads(Data)["pic_urls"]:
					for img in i.values():
						 GetImg(os.path.split(os.path.realpath(__file__))[0]+"/DB/"+str(j[0])+"--"+os.path.split(img)[1],re.sub("(/bmiddle/)|(/thumbnail/)","/large/",img))
			except:
				pass
			if eml.send_mail(["admin@nkucodingcat.com"],"SomeOne Update a MicroBlog","It happened @ "+j[1]["created_at"]+"\n"+j[1]["text"]):
				print "Mail Sent"
			else:
				print "Mail Sent Failed"
def GetImg(Loc,url):
	f = open(Loc,"wb")
	f.write(urllib2.urlopen(url).read())
	f.close()
def GetMicroBlog(id,head):
	Req = urllib2.Request("""https://api.weibo.com/2/statuses/show.json?id="""+str(id),headers=head)
	return urllib2.urlopen(Req).read()
def GetTimeLine(head,Self,Target):
	count = 1
	while True:
		Req = urllib2.Request("""https://api.weibo.com/2/statuses/friends_timeline.json?count=100&page="""+str(count),headers=head)
		S = json.loads(urllib2.urlopen(Req).read())["statuses"]
		yield [[[i["id"],i] for i in S if i["user"]["id"] == Target],[t2.Tran_Weibo_Ts(j["created_at"]) for j in S if j["user"]["id"] == Self]]
		count += 1
def GetBilTimeLine(head,Self,Target):
	count = 1
	while True:
		Req = urllib2.Request("""https://api.weibo.com/2/statuses/bilateral_timeline.json?count=100&page="""+str(count),headers=head)
		S = json.loads(urllib2.urlopen(Req).read())["statuses"]
		yield [[[i["id"],i] for i in S if i["user"]["id"] == Target],[t2.Tran_Weibo_Ts(j["created_at"]) for j in S if j["user"]["id"] == Self]]
		count += 1
def GetPage(head,Self,Target):
	Now = time.mktime(datetime.datetime.fromtimestamp(time.time(),tz=t2.GMT8()).timetuple())
	Need = {}
	for i in GetTimeLine(head,Self,Target):
		for k in i[0]:
			Need[k[0]] = k[1]
		if i[1]:
			if (i[1][-1] < (Now - 60*60*1.5)):
				break
	for i in GetTimeLine(head,Self,Target):
		for k in i[0]:
			Need[k[0]] = k[1]
		if i[1]:
			if (i[1][-1] < (Now - 60*60*1.5)):
				break
	return Need.items()
begin() 

