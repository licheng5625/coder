__author__ = 'licheng5625'
from bs4 import BeautifulSoup
import urllib.request
import zlib
import os
import json
import time
import datetime

class SnoperCrawler:
    __mydictdata =list()
    __lastname=str()
    listoflink=set()
    listofsavedlink=set()
    __path=str()
    def __getData(self,websitepage):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
        url=opener.open('http://www.snopes.com/info/whatsnew.asp?page='+str(websitepage)).read()
        return zlib.decompress(url, 16+zlib.MAX_WBITS)
    def __saveWebpage(self,path,filename,data):
        with open(path+filename, encoding='utf-8', mode='w+') as reporter:
            reporter.write(data)

    def CrawOnePage(self,websitepage=1,issave = True):
        decompressed_data=self.__getData(websitepage)
        #print (decompressed_data.decode('utf-8'))
        #url= urllib.request.urlopen().read()

        soup = BeautifulSoup(decompressed_data)
        #soup = BeautifulSoup(open("/Users/licheng5625/Desktop/What's New _ snopes.com.htm"))

        #fff=soup.find_all("a","img-wrapper")

        postlist =soup.find(attrs={"class": "post-list"})
        items=postlist.find_all("li")
        for item in items:
            onepost=item.find("span","label")
            if onepost is not None:
                i=len(self.__mydictdata)
                print ('NO:'+ str(i))
                link=item.find(attrs={"class": "title"}).find('a') .get('href')
                fulllink ="http://www.snopes.com"+link
                if not fulllink =='http://www.snopes.com//':
                    print (fulllink)
                    print (onepost.text)
                    if (fulllink not in self.listofsavedlink):
                        self.__CrawPages(fulllink,link)
                        #contentdict=self.__CrawContent(fulllink,onepost.text,issave)
                        #if contentdict is not None:
                        #    self.__mydictdata.append(contentdict)
                        #    self.listoflink.add(link)

    def __CrawPages(self,fulllink,link):
        url2= urllib.request.urlopen(fulllink).read().decode('utf-8')
        self.__saveWebpage('webpages/',link.replace('/','')+'.html',url2)
        self.listofsavedlink.add(fulllink)
    def Writelog(self,path='',filename='log.txt'):
         with open(path +filename , encoding='utf-8', mode='w+') as reporter:
             for onestory in self.listofsavedlink:
                reporter.write(onestory + '\n')
    def ReadLog(self,path=''):
        try:
             with open('webpages/pagesavedlist.txt', encoding='utf-8', mode='r') as Seenlist:
                for line in Seenlist:
                    self.listofsavedlink.add(line.replace('\n', ''))
             with open(path + 'webpages/blacklist.txt', encoding='utf-8', mode='r') as blacklist:
                for line in blacklist:
                    self.listoflink.add(line.replace('\n', ''))
        except FileNotFoundError:
             with open('webpages/blacklist.txt', encoding='utf-8', mode='w+') as Seenlist:
                 Seenlist.write('')
             with open('webpages/pagesavedlist.txt', encoding='utf-8', mode='w+') as Seenlist:
                 Seenlist.write('')
    def gettimestamp(self):
        format_type = u'%Y_%m_%d_%H_%M_%S'
        return time.strftime(format_type, time.localtime(time.time()))
s=SnoperCrawler()
s.ReadLog()
for i in range(1,99):
    try:
        s.CrawOnePage(i)
    except:
        s.Writelog('webpages',filename='pagesavedlist.txt')
