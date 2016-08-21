__author__ = 'licheng5625'
from bs4 import BeautifulSoup
import urllib.request
import zlib
import os
from time import sleep

import path
import json
from fake_useragent import UserAgent

class UserCrawler:
    __mydictdata =list()
    _lastname=str()
    listoflink=set()
    listofsavedlink=set()
    ua = UserAgent()
    header=list()
    def _getHeader(self):
        self.header=[('User-agent', self.ua.random),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
    def __getData(self,username):
        opener = urllib.request.build_opener()
        if len(self.header) ==0:
            self._getHeader()
        opener.addheaders = self.header #[('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
        url=opener.open('https://twitter.com/'+username).read()
        return zlib.decompress(url, 16+zlib.MAX_WBITS)
    def __saveWebpage(self,path,filename,data):
        with open(path+filename, encoding='utf-8', mode='w+') as reporter:
            reporter.write(data)

    def CrawPage(self,username,counter=0):
        try:
            decompressed_data=self.__getData(username)
            soup = BeautifulSoup(decompressed_data)
            headcard = soup.find("div", class_="ProfileHeaderCard")
            if headcard is None:
                counter=counter+1
                if counter <4:
                    self._getHeader()
                    self.CrawPage(username,counter)
                else:
                   with open(path.userrawpath +'canfindhard.txt', encoding='utf-8', mode='a') as Seenlist:
                       Seenlist.write(username+'\n')

            self.__saveWebpage(path.userrawpath+'News/',username+'.html',decompressed_data.decode('utf-8'))
            with open(path.userrawpath +'pagesavedlist.txt', encoding='utf-8', mode='a') as Seenlist:
                Seenlist.write(username+'\n')
        except urllib.error.HTTPError:
            counter=counter+1
            if counter <4:
                sleep(4)
                self._getHeader()
                self.CrawPage(username,counter)
            else:
                 with open(path.userrawpath +'blacklist.txt', encoding='utf-8', mode='a') as Seenlist:
                    Seenlist.write(username+'\n')
        #print (decompressed_data.decode('utf-8'))
        #url= urllib.request.urlopen().read()

        #soup = BeautifulSoup(decompressed_data)
        #soup = BeautifulSoup(open("/Users/licheng5625/Desktop/What's New _ snopes.com.htm"))

        #fff=soup.find_all("a","img-wrapper")
    def CrawPages(self):
         self._getHeader()
         with open(path.USerJSONpath+'simple_News_UserJson.txt', encoding='utf-8', mode='r') as Seenlist:
            for line in Seenlist:
                self.listoflink.add(json.loads(line)['screen_name'])
         for link in self.listoflink:
            if link not in self.listofsavedlink:
                print(link)
                self.CrawPage(link)
                self.listofsavedlink.add(link)


    def ReadLog(self):
        try:
             with open(path.USerJSONpath+'User_JSON.txt', mode='r')as Seenlist2:
                for line in Seenlist2:
                    user=json.loads(line)
                    self.listofsavedlink.add(user['user_screen_name'])
             for  root, dirs, files in os.walk(path.userrawpath+'News'):
                for name in files:
                    if ('html' not in name) :
                        continue
                    self.listofsavedlink.add(name.replace('.html', ''))
             with open(path.userrawpath + 'blacklist.txt', encoding='utf-8', mode='r') as blacklist:
                for line in blacklist:
                    self.listofsavedlink.add(line.replace('\n', ''))
        except FileNotFoundError:
             with open(path.userrawpath +'blacklist.txt', encoding='utf-8', mode='a') as Seenlist:
                 Seenlist.write('')


s=UserCrawler()
s.ReadLog()
s.CrawPages( )
#s.CrawPage('mellyxoh')