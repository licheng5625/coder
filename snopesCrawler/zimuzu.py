__author__ = 'licheng5625'
from bs4 import BeautifulSoup
import urllib.request
import zlib
import http.cookiejar
import json
import time
import datetime
class Autologin:
    def lognin(self):
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch"),('Cookie','PHPSESSID=bt9pj6jqimimkidfbv4scub5k5; zmz_rich=1; GINFO=uid=3471489&nickname=licheng5625&group_id=1&avatar_t=&main_group_id=0&common_group_id=54; GKEY=d887a2b1c893f098bcbe48aafeb25dc4')]

        data = urllib.parse.urlencode({'account':'licheng5625','password':5625046,'remember':1,'url_back':'http://www.zimuzu.tv'})
        data = data.encode('ascii')
        url=opener.open("http://www.zimuzu.tv/User/Login/ajaxLogin", data) .read()
        for ck in cj:
            if ck.name == 'GKEY':
                return ck.value
        return None
    def getData(self):
        GKEY=self.lognin()
        if GKEY is not None:
            opener = urllib.request.build_opener()
            cookiestr='PHPSESSID=bt9pj6jqimimkidfbv4scub5k5; zmz_rich=1; GINFO=uid=3471489&nickname=licheng5625&group_id=1&avatar_t=&main_group_id=0&common_group_id=54; GKEY='+GKEY
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch"),('Cookie',cookiestr)]
            url=opener.open('http://www.zimuzu.tv/user/sign').read()
            return zlib.decompress(url, 16+zlib.MAX_WBITS)
        else:
            return None
s =Autologin()
#s.lognin()
soup = BeautifulSoup(s.getData())
#print (soup)
div2= soup.find('div',"a2 tc")
if div2 is not None:
    days=div2.find('font','f2').text
    print ('There is '+str(days)+'days')
else:
    print ('can\'t login in')
