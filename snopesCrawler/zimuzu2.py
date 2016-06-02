from __future__ import absolute_import
__author__ = u'licheng5625'
from bs4 import BeautifulSoup
import urllib2, urllib
import zlib
import cookielib
import json
import time
import datetime
class Autologin(object):
    def lognin(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [(u'User-agent', u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),(u'DNT', u"1"),(u'Accept-Language', u"en-US;q=0.8,en;q=0.2"),(u'Accept-Encoding', u"gzip, deflate, sdch"),(u'Cookie',u'PHPSESSID=bt9pj6jqimimkidfbv4scub5k5; zmz_rich=1; GINFO=uid=3471489&nickname=licheng5625&group_id=1&avatar_t=&main_group_id=0&common_group_id=54; GKEY=d887a2b1c893f098bcbe48aafeb25dc4')]

        data = urllib.urlencode({u'account':u'licheng5625',u'password':5625046,u'remember':1,u'url_back':u'http://www.zimuzu.tv'})
        data = data.encode(u'ascii')
        url=opener.open(u"http://www.zimuzu.tv/User/Login/ajaxLogin", data) .read()
        for ck in cj:
            if ck.name == u'GKEY':
                return ck.value
        return None
    def getData(self):
        GKEY=self.lognin()
        if GKEY is not None:
            opener = urllib2.build_opener()
            cookiestr=u'PHPSESSID=bt9pj6jqimimkidfbv4scub5k5; zmz_rich=1; GINFO=uid=3471489&nickname=licheng5625&group_id=1&avatar_t=&main_group_id=0&common_group_id=54; GKEY='+GKEY
            opener.addheaders = [(u'User-agent', u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),(u'DNT', u"1"),(u'Accept-Language', u"en-US;q=0.8,en;q=0.2"),(u'Accept-Encoding', u"gzip, deflate, sdch"),(u'Cookie',cookiestr)]
            url=opener.open(u'http://www.zimuzu.tv/user/sign').read()
            return zlib.decompress(url, 16+zlib.MAX_WBITS)
        else:
            return None
s =Autologin()
#s.lognin()
soup = BeautifulSoup(s.getData())
#print (soup)
div2= soup.find(u'div',u"a2 tc")
if div2 is not None:
    days=div2.find(u'font',u'f2').text
    print u'There is '+unicode(days)+u'days'
else:
    print u'can\'t login in'
