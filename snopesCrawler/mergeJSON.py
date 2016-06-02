__author__ = 'licheng5625'
from bs4 import BeautifulSoup
import urllib.request
import zlib
import os
import json
import time
import datetime


def Writelog(path='',filename='log.txt'):
     with open(path +filename , encoding='utf-8', mode='w+') as reporter:
         for onestory in self.listoflink:
            reporter.write(onestory + '\n')
def ReadLog(content):
     with open( 'jounral.txt', encoding='utf-8', mode='a') as Seenlist:
        Seenlist.write(content + '\n')
setofrumors=set()
for  root, dirs, files in os.walk("./"):
    for name in files:
        if root =='./webpages':
            continue
        path = root  + name
        if ('journal'  in name):
            with open(path, encoding='utf-8', mode='r') as Seenlist:
                for line in Seenlist:
                    datajson=json.loads(line)
                    if datajson["link"].rstrip('/') not in setofrumors:
                        setofrumors.add(datajson["link"].rstrip('/'))
                        with open( 'jounral.txt', encoding='utf-8', mode='a') as Seenlist2:
                            Seenlist2.write(line )