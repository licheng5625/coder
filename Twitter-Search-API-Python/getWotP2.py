from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
from io import open
import urllib2, urllib, urlparse
import urllib2, urllib
import urllib2, urllib
import json
import path
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import requests
import fuckCaptcha

import random
import httplib
import socket

def urlremain(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return True
    except urllib2.URLError:
        return False

def getWotScore(url):
    ulrwot=u'http://api.mywot.com/0.4/public_link_json2?hosts='+url+u'&key=373fe6c5f2a19ef6841fb3965fd06f480d975e1e'
    req = urllib2.Request(ulrwot)
    response = urllib2.urlopen(req).read().decode(u'utf-8')
    return response


# Json = json.loads(getWotScore('http://bit.ly/1HXqx4O'))
# print(Json['bit.ly']['0'][0])


# proto, rest = urllib.parse("docs.python.org/dsds")
# res, rest = urllib.splithost(rest)
# print ("unkonw" if not res else res)

UlrWot=dict()
listofproxy=[]
with open(path.datapath+u'proxylist.txt',mode=u'r') as pro:
    for line in pro:
        listofproxy.append(json.loads(line.replace(u"\n",u'')))

with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'URLsRumors.txt', mode=u'r')as Seenlist2:
     for line in Seenlist2:
         line=line.replace(u"\n",u'')
         UlrWot[line]=0

with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'URLs.txt', mode=u'r')as Seenlist2:
     for line in Seenlist2:
         line=line.replace(u"\n",u'')
         UlrWot[line]=0
with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'URLsBBC.txt', mode=u'r')as Seenlist2:
     for line in Seenlist2:
         line=line.replace(u"\n",u'')
         UlrWot[line]=0

with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'WOtURLs.txt', mode=u'r')as Seenlist2:
     for line in Seenlist2:
         line=line.replace(u"\n",u'').split(u"   ")
         UlrWot[line[0]]=line[1]
def getHeader():
    ua = UserAgent()
    header={u'User-agent': ua.random,u'DNT': u"1",u'Accept-Language': u"en-US;q=0.8,en;q=0.2",u'Accept-Encoding': u"deflate, sdch"}
    return header    

            # proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            #
            # opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # opener.addheaders =[('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
            # opener.open('http://www.google.com').read()
            #res = conn.getresponse()
       # except socket.gaierror:


#proxies=getProxy()
def getRanknoproxy(url):
    #opener = urllib.request.build_opener()
    # header=getHeader()
    # if len(header) ==0:
    #     header=getHeader()
    #proxies=getProxy()
    try:
        data=requests.get(u'http://www.alexa.com/siteinfo/'+url).text
        return phaseAlexa(data)
    except Exception:
        print u'getRank error'

        return u'error'

def getRank(url,proxies):
    #opener = urllib.request.build_opener()
    # header=getHeader()
    # if len(header) ==0:
    #     header=getHeader()
    #proxies=getProxy()
    try:
        data=requests.get(u'http://www.alexa.com/siteinfo/'+url,proxies=proxies).text
        return phaseAlexa(data)
    except Exception:
        print u'getRank error'

        return u'error'
    #data=opener.open('http://www.alexa.com/siteinfo/'+url).read()
    #data=data.decode('utf-8')

#16,852,849"
def getNum(numstring):
    numberstr=u'0123456789.'
    tempstr=numstring
    for char in numstring:
        if char not in numberstr:
            tempstr=tempstr.replace(char,u'')
    return int(tempstr)
def phaseAlexa(html):
    css_soup = BeautifulSoup(html)

    #css_soup.select(".align-vmiddle")
    rank= css_soup.select(u".change-r2")[0].parent.strong.text.replace(u'\n',u'')
    try:
        return getNum(rank)
    except ValueError:
        return 20000000


def getTypenoproxy(url,captcha=None):
    #proxies=getProxy()
    try:
        header=getHeader()
        r=None
        url=unicode(u"http://sitereview.bluecoat.com/rest/captcha.jpg?1470834655096")
        result= fuckCaptcha.distinguish_captcha(url)

        if captcha==None:
            r = requests.post(u'http://sitereview.bluecoat.com/rest/categorization', data = {u'url':url},headers=header,timeout=4)
        else:
            print (u"get type with captcha"+unicode(captcha))
            r = requests.post(u'http://sitereview.bluecoat.com/rest/categorization', data = {u'url':url,u'captcha':captcha},headers=header,timeout=4)
        data=r.json()
        return phaseTypes(url,data)

    except Exception, e:
        print unicode(proxy)+unicode(e)

        return u'error'
def getType(url,proxies):
    #proxies=getProxy()
    try:
        header=getHeader()
        r = requests.post(u'http://sitereview.bluecoat.com/rest/categorization', data = {u'url':url},proxies=proxies,headers=header,timeout=4)
        print (u"get type with proxy"+unicode(proxies))
        data=r.json()
        return phaseTypes(url,data)

    except Exception:

        # postdata = urllib.parse.urlencode({'url': url})
        # postdata = postdata.encode('utf-8')
        #
        # response = urllib.request.urlopen('http://sitereview.bluecoat.com/rest/categorization',postdata)
        # text =response.read().decode('utf-8')
        # time.sleep('15')
        return u'error'

     #return phaseTypes(url,)
     #return phaseTypes(data)

def phaseTypes(url,html):
    rank =u"no type"
    print html
    try:
        if not html[u'unrated']:
            css_soup = BeautifulSoup(html[u'categorization'])
            #print(html['categorization'])
            #css_soup.select(".align-vmiddle")
            try:
                rank= css_soup.find_all(u"a")[1].text#.findall('a')
            except IndexError:
                rank= css_soup.find_all(u"a")[0].text
    except KeyError:
        #r = requests.post('http://sitereview.bluecoat.com/rest/categorization', data = {'url':url},headers=header,timeout=4)
        #print(r.json())
        #getTypenoproxy(url,captcha=result)

        print u'phaseTypes error'
        return u'error'
    print rank
    return rank
#getType('www.asdasdsafasfaf.com')
listofweb=[]
with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'WOtURLs2.txt', mode=u'r')as Seenlist2:
    for line in Seenlist2:
        url=json.loads(line)[u'url']
        listofweb.append(url)

blacklistproxy=set()
def getProxy():
        global blacklistproxy
        print u'change proxy'
        proxy=None
        while proxy==None:
            try:
                proxy=random.choice(listofproxy)
                while proxy[u'proto']==u'https' or proxy[u'url'] in blacklistproxy:
                    assert len(listofproxy)>len(blacklistproxy)
                    proxy=random.choice(listofproxy)
                # proxies = {
                #     proxy.split('://')[0]:proxy}
                proxies={proxy[u'proto']:proxy[u'url']}
                #print(proxies)
                requests.get(u'http://www.alexa.com/siteinfo/'+u'google.com',proxies=proxies,timeout=4)
                proxy = proxies
            except Exception, e:
                blacklistproxy.add(proxy[u'url'])
                print (float(len(blacklistproxy))/len(proxy))
                #print(str(proxy)+str(e))
                return None
        print (u'pick:'+unicode(proxy))
        return proxy
#'http': 'http://111.13.136.36:80'
#'http': 'http://120.198.248.97:80'
#http://80.112.170.75:80
#'http': 'http://103.27.24.236:83'
#http://123.126.32.102:8080
with open(path.datapath+u'/webpagefortwitter/Tweet_JSON/'+u'WOtURLs2.txt', mode=u'a')as Seenlist2:
        wotdict=dict()
        proxies=None
        # while proxies==None:
        #     proxies=getProxy()
        count=0
        for key in list(UlrWot.keys()):
            if key not in listofweb:
                print (unicode(len(listofweb)+count)+u"--------"+unicode(len(UlrWot)))
                count+=1
                wotdict[u'type']=getTypenoproxy(key)
                while wotdict[u'type']==u'error':
                    wotdict[u'type']=getTypenoproxy(key)

                    # blacklistproxy.add(proxies['http'])
                    # proxies=None
                    # while proxies==None:
                    #     proxies=getProxy()
                    # wotdict['type']=getType(key,proxies)
                wotdict[u'rank']=getRanknoproxy(key)#,proxies)
                while wotdict[u'rank']==u'error':
                    blacklistproxy.add(proxies[u'http'])
                    proxies=None
                    while proxies==None:
                        proxies=getProxy()
                    wotdict[u'rank']=getRank(key,proxies)
                wotdict[u'url']=key
                if UlrWot[key]!=0:
                    Json = json.loads(getWotScore(key+u'/'))
                    try:
                        wotdict[u'wot']=Json[key][u'0'][0]
                    except KeyError:
                        wotdict[u'wot']=0
                else:
                        wotdict[u'wot']=0

                Seenlist2.write(json.dumps(wotdict)+u"\n")


# proxies=None
# while proxies==None:
#     proxies=getProxy()
# print(proxies)
# header=getHeader()
# data=requests.get('http://www.whatsmyip.org/more-info-about-you/',proxies=proxies,headers=header).text
# print(data)