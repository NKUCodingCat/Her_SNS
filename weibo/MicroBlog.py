#!/usr/bin/python
# -*- coding: utf-8 -*-
#from weibopy.api import API
from weibo import APIClient
import re, sys,os,urllib,urllib2,cookielib,httplib,time,datetime,json,t2
import webbrowser
import urlparse

#模拟授权并且获取回调地址上的code，以获得acces token和token过期的UNIX时间
APP_KEY = 'xxxxxxxxx' # app key
APP_SECRET = 'xxxxxxxxxxxxxxxxxx' # app secret
#回调地址，可以用这个默认地址
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html' 
def get_code(): 

	AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
	USERID = 'xxxxxxxxxxxxxxx' #微博账号
	PASSWD = 'xxxxxxxxxxxxxxx' #微博密码
	
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
	client.statuses.update.post(status=num)
	#私人需求
	head = {"Authorization":"OAuth2 "+access_token}
	DB = os.listdir(os.path.split(os.path.realpath(__file__))[0]+"/DB")
	Need = GetPage(head,<a Long int>)
	for j in Need:
		if True or str(j)+".json" not in DB:
			Data = GetMicroBlog(j,head)
			f = open(os.path.split(os.path.realpath(__file__))[0]+"/DB/"+str(j)+".json","w")
			f.write(Data)
			f.close()
			try:
				for i in json.loads(Data)["pic_urls"]:
					for img in i.values():
						 GetImg(os.path.split(os.path.realpath(__file__))[0]+"/DB/"+str(j)+"--"+os.path.split(img)[1],re.sub("(/bmiddle/)|(/thumbnail/)","/large/",img))
			except:
				pass
def GetImg(Loc,url):
	f = open(Loc,"wb")
	f.write(urllib2.urlopen(url).read())
	f.close()
def GetMicroBlog(id,head):
	Req = urllib2.Request("""https://api.weibo.com/2/statuses/show.json?id="""+str(id),headers=head)
	return urllib2.urlopen(Req).read()
def GetPage(head,Target):
	Need = []
	Req = urllib2.Request("""https://api.weibo.com/2/statuses/friends_timeline.json?count=100""",headers=head)
	S = json.loads(urllib2.urlopen(Req).read())["statuses"]
	Need += [i["id"] for i in S if i["user"]["id"] == Target]
	Req = urllib2.Request("""https://api.weibo.com/2/statuses/bilateral_timeline.json?count=100""",headers=head)
	S = json.loads(urllib2.urlopen(Req).read())["statuses"]
	Need += [i["id"] for i in S if i["user"]["id"] == Target]
	return list(set(Need))
begin() 

