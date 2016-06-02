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
                    if (fulllink not in self.listoflink):
                        #self.__CrawPages(fulllink,link)
                        contentdict=self.__CrawContent(fulllink,link,onepost.text,issave)
                        if contentdict is not None:
                            self.__mydictdata.append(contentdict)
                            self.listoflink.add(link)

    def __CrawPages(self,fulllink,link):
        url2= urllib.request.urlopen(fulllink).read().decode('utf-8')
        self.__saveWebpage('./webpages/',link.replace('/','')+'.html',url2)
        self.Writelog('./webpages/',filename='pagesavedlist.txt')
        self.listofsavedlink.add(fulllink)
    def __CrawContent(self,fulllink,link,kind,issave):
        mydict = dict()
        mydict["Label"]=kind
        url2= urllib.request.urlopen(fulllink).read()
        if issave:
            self.__saveWebpage('./webpages/',link.replace('/',''),url2.decode('utf-8'))
        soup2 = BeautifulSoup(url2)
        kindlist =soup2.find_all('li',itemprop="itemListElement")
        kind=''
        for kind2 in kindlist:
            if kind2.a is not None and kind2.a.get('href') =="/category/facts/":
                  kind ='FACT CHECK'
        if   kind != 'FACT CHECK':
            kind ='NEWS'
            print ('NEWS')
        mydict["Label"]=kind
        headline=soup2.find("h1", {'class',"page-title"}).text
        mydict["headline"]=headline
        mydict["link"]=link
        description=soup2.find("h2","article-description").text
        mydict["description"]=description
        if kind !='NEWS':
            if len(soup2.find_all("div","claim-old old-mfalse"))!=0 or len(soup2.find_all('img',{"src" : "/images/mostlyfalse.gif"}))!=0 :
                print ('result: MOSTLY FALSE' )
                mydict["Result"]="MOSTLY FALSE"
            else:
                if len(soup2.find_all("div","claim-old old-false"))!=0 or soup2.find('img',{"src" : "/images/false.gif"}) is not None or soup2.find('img',src="http://m.snopes.com/wp-content/uploads/2015/05/false.gif") is not None:
                    print ('result: FALSE' )
                    mydict["Result"]="FALSE"
                else:
                    if len(soup2.find_all("div","claim-old old-mixture"))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/mixture.png"}))!=0 or len(soup2.find_all('img',{"src" : "/images/mixture.gif"}))!=0:
                        print ('result: MIXTURE' )
                        mydict["Result"]="MIXTURE"
                    else:
                        if len(soup2.find_all("div","claim-old old-undetermined"))!=0 or len(soup2.find_all("div","claim-old old-legend"))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/undetermined.png"}))!=0 or len(soup2.find_all('img',src="/images/yellow.gif"))!=0:
                            print ('result: UNDETERMINED' )
                            mydict["Result"]="UNDETERMINED"
                        else:
                            if len(soup2.find_all("div","claim-old old-mtrue"))!=0  or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/mostlytrue.png"}))!=0 or len(soup2.find_all('img',{"src" : "/images/mostlytrue.gif"}))!=0:
                                print ('result: MOSTLY TRUE' )
                                mydict["Result"]="MOSTLY TRUE"
                            else:
                                if len(soup2.find_all("div","claim-old old-mostlyfalse"))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/mostlyfalse.png"}))!=0:
                                    print ('result: MOSTLY FLASE' )
                                    mydict["Result"]="MOSTLY FLASE"
                                else:
                                    if len(soup2.find_all('img',{"src" : "/images/red.gif"}))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/false.png"}))!=0:
                                        print ('result: FALSE' )
                                        mydict["Result"]="FALSE"
                                    else:
                                        if len(soup2.find_all('img',{"src" : "/images/green.gif"}))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/true.png"}))!=0 or len(soup2.find_all('img',{"src" : "http://www.snopes.com/images/m/TRUE.png"}))!=0:
                                            print ('result: TRUE' )
                                            mydict["Result"]="TRUE"
                                        else:
                                            if len(soup2.find_all('img',{"src" : "/images/legend.gif"}))!=0:
                                                print ('result: legend' )
                                                mydict["Result"]="legend"
                                            else:
                                                flasetext=soup2.find("font",{'class':"sect_font_style",'color':'#FF0000'})
                                                if flasetext is not None and flasetext.b.i.text == 'False.':
                                                    print ('result: False' )
                                                    mydict["Result"]="False"
                                                else:
                                                    #raise ValueError('don\'t know the result ')
                                                    with open('unknownResult.txt', encoding='utf-8', mode='a') as reporter:
                                                        reporter.write(link + '\n')
                                                    return None

        clams=soup2.find_all("span","green-label")
        for clam in clams:
            if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim' :
                clamtext=clam.next_sibling
                print (str(type(clamtext)))
                if not  str(type(clamtext))  == '<class \'bs4.element.NavigableString\'>' :
                    clamtext=clam.next_sibling.text
                clamtext=clamtext.replace('Claim: ','')
                print (clamtext.encode('utf-8'))
                mydict["Claim"]=clamtext

            if clam.text =='Originally published:':
                timetext =  clam.parent.text.replace("Originally published:","").replace('\n',' ').replace(u'\xa0',' ').strip(' ').rstrip('f')
                time = datetime.datetime.strptime(timetext,"%d %B %Y")
                print ("Originally published: "+time.strftime("%d %B %Y"))
                mydict["Originally published Time"]=time.strftime("%d %B %Y")
        if "Claim" not in mydict.keys() and kind !='NEWS':
            clams=soup2.find_all("font","copyright_text_color_g")
            for clam in clams:
                b=clam.find("b")
                if (b is not None and (b.text == 'Claim:' or b.text ==  'Scam:' or b.text == 'Phishing bait:')):
                    clamtext=clam.parent.text.replace('Claim: ','').split('\n')[1]
                    mydict["Claim"]=clamtext
                    print (clamtext.encode('utf-8'))
                if b is not None and b.text == 'Last updated:':
                    timetext =  clam.next_sibling.replace('\n','').replace(u'\xa0',' ').strip(' ').replace('\r','')
                    print (timetext.encode('utf-8'))
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))
                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
                strong =clam.find("strong")
                if (strong is not None and strong.text == 'Claim:') :
                    clamtext=clam.parent.text.replace('Claim: ','').split('\n')[1]
                    mydict["Claim"]=clamtext
                    print (clamtext.encode('utf-8'))
                if strong is not None and strong.text == 'Last updated:':
                    timetext =  clam.next_sibling.replace('\n','').replace(u'\xa0',' ').strip(' ').replace('\r','')
                    print (timetext.encode('utf-8'))
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))
                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
            clams=soup2.find_all("font","copyright_text_color")
            for clam in clams:
                b=clam.find("b")
                if b is not None and b.text == 'Claim:':
                    clamtext=clam.parent.text.replace('Claim: ','').split('\n')[1]
                    mydict["Claim"]=clamtext
                    print (clamtext.encode('utf-8'))
                if b is not None and b.text == 'Last updated:':
                    timetext =  clam.next_sibling.replace('\n','')
                    time = datetime.datetime.strptime(timetext," %d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))
                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
        if "Originally published Time" not in mydict.keys():
            bs=soup2.find_all("b")
            for b in bs:

                if b.text=='Last updated:':
                    timetext =  b.parent.next_sibling.replace('\n','').replace(u'\xa0',' ').strip(' ').replace('  ','')
                    if timetext !='':
                        time = datetime.datetime.strptime(timetext,"%d %B %Y")
                        print ("Originally published: "+time.strftime("%d %B %Y"))
                        mydict["Originally published Time"]=time.strftime("%d %B %Y")

        clams=soup2.find_all("span",style="color: #1aa315;")
        if len(clams) != 0 :
            for clam in clams:
                if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim':
                    clamtext=clam.parent.next_sibling.replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
                b=clam.b
                if b is not None and b.span is not None and b.span.text == 'Claim:':
                    clamtext=clam.next_sibling.replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
                if b is not None and b.text == 'Last updated:':
                    timetext =  clam.next_sibling.replace('\n','').replace(u'\xa0',' ').strip(' ').replace('\r','')
                    print (timetext.encode('utf-8'))
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))
                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
        clams=soup2.find_all("span",style="color: #1aa315; font-weight:bold;")
        if len(clams) ==0:
            clams=soup2.find_all("span",style="color: #1aa315; font-weight:bold")
        if len(clams) != 0 :
            for clam in clams:
                if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim':
                    clamtext=clam.parent.text.replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
                if clam.text == 'Last updated:':
                    timetext =  clam.next_sibling.replace('\n','').replace(u'\xa0',' ').strip(' ').replace('\r','')
                    print (timetext.encode('utf-8'))
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))
                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
        clams=soup2.find_all("span",{'style',"color: #1aa315;"})
        if len(clams) != 0 :
            for clam in clams:
               if clam.text == 'Claim:' or clam.text == 'NEWS:':
                    clamtext=clam.next_sibling.text.replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
        clams=soup2.find_all("span",style="color: #1aa315;  font-weight: bold;")
        if len(clams) != 0 :
            for clam in clams:
               if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim' :
                    clamtext=clam.next_sibling
                    if clamtext is None:
                        clamtext=clam.parent.next_sibling
                    clamtext=clamtext .replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
        clams=soup2.find_all("span",style="color: #1aa315; font-size: 125%;")
        if len(clams) != 0 :
            for clam in clams:
               if clam.text == 'Claim:' or clam.text == 'NEWS:':
                    clamtext=clam.next_sibling
                    if clamtext is None:
                        clamtext=clam.parent.next_sibling
                    clamtext=clamtext .replace('Claim: ','')
                    print (clamtext.encode('utf-8'))
                    mydict["Claim"]=clamtext
        clams=soup2.find_all("span",style="color: #1aa315; font-weight: bold; font-size: large;")
        for clam in clams:
            if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim':
                clamtext=clam.next_sibling
                print (clamtext.encode('utf-8'))
                mydict["Claim"]=clamtext
            if "Originally published Time" not in mydict.keys():
                if clam.text == 'Last updated:':
                        timetext=clam.next_sibling.replace(u'\xa0',' ').strip(' ').rstrip('f')
                        time = datetime.datetime.strptime(timetext,"%d %B %Y")
                        print ("Originally published: "+time.strftime("%d %B %Y"))
                        mydict["Originally published Time"]=time.strftime("%d %B %Y")
        clams=soup2.find_all("span",style="color: #1aa315; font-weight: bold;")
        if len(clams)==0:
            clams=soup2.find_all("span",style="color: #1aa315; font-weight: bold")
        for clam in clams:
            if clam.text == 'Claim:' or clam.text == 'NEWS:' or clam.text == 'Claim':
                clamtext=clam.next_sibling
                if clamtext is None:
                    clamtext=clam.parent.next_sibling
                print (clamtext.encode('utf-8'))
                mydict["Claim"]=clamtext
        if "Originally published Time" not in mydict.keys():
            timelist=soup2.find_all("span",style="color: #1aa315; font-weight: bold;")
            for times in timelist:
                if times.text == 'Last updated:':
                    timetext=times.next_sibling.replace(u'\xa0',' ').strip(' ').rstrip('f')
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))

                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
        if "Originally published Time" not in mydict.keys():
            timelist=soup2.find_all("span",style="color: #1aa315; font-weight: bold")
            for times in timelist:
                if times.text == 'Last updated:':
                    timetext=times.next_sibling.replace(u'\xa0',' ').strip(' ').rstrip('f')
                    time = datetime.datetime.strptime(timetext,"%d %B %Y")
                    print ("Originally published: "+time.strftime("%d %B %Y"))

                    mydict["Originally published Time"]=time.strftime("%d %B %Y")
        taglist=soup2.find("div","article-tags clearfix")
        print ("tags:")
        tagtextlist =list()
        if taglist is not None:
            tags =taglist.find_all("a")
            for tag in tags:
                tagtextlist.append(tag.text)
                print (tag.text.encode('utf-8'))
        mydict["Tags"]=tagtextlist
        if "Claim" not in mydict.keys() and kind !='NEWS':
            with open('unknownClaim.txt', encoding='utf-8', mode='a') as reporter:
                reporter.write(link + '\n')
            return None
        if "Originally published Time" not in mydict.keys() and kind !='NEWS':
            with open('unknownTime.txt', encoding='utf-8', mode='a') as reporter:
                reporter.write(link + '\n')
            return None
        self.listoflink.add(link)
        return mydict

    def __MakeJSON(self,mydic):
            JSON = json.dumps(mydic, ensure_ascii=False)
            return JSON
    def WriteJSON(self,path=''):
        try:
            os.remove(path+self.__lastname)
        except FileNotFoundError:
            pass
        finally:
            self.__lastname =path + 'journal' + self.gettimestamp() + '.txt'
            with open(self.__lastname, encoding='utf-8', mode='w+') as reporter:
                for onestory in self.__mydictdata:
                    JSON = self.__MakeJSON(onestory)
                    reporter.write(JSON + '\n')
            self.Writelog()
    def Writelog(self,path='',filename='log.txt'):
         with open(path +filename , encoding='utf-8', mode='w+') as reporter:
             for onestory in self.listoflink:
                reporter.write(onestory + '\n')
    def ReadLog(self,path=''):
        try:
             with open(path + 'log.txt', encoding='utf-8', mode='r') as Seenlist:
                for line in Seenlist:
                    self.listoflink.add(line.replace('\n', ''))
             with open('./webpages/pagesavedlist.txt', encoding='utf-8', mode='r') as Seenlist:
                for line in Seenlist:
                    self.listofsavedlink.add(line.replace('\n', ''))
             with open(path + 'blacklist.txt', encoding='utf-8', mode='r') as blacklist:
                for line in blacklist:
                    self.listoflink.add(line.replace('\n', ''))
        except FileNotFoundError:
             with open(path + 'log.txt', encoding='utf-8', mode='w+') as Seenlist:
                 Seenlist.write('')
             with open(path +'blacklist.txt', encoding='utf-8', mode='a') as Seenlist:
                 Seenlist.write('')
             with open('./webpages/pagesavedlist.txt', encoding='utf-8', mode='a') as Seenlist:
                 Seenlist.write('')
    def gettimestamp(self):
        format_type = u'%Y_%m_%d_%H_%M_%S'
        return time.strftime(format_type, time.localtime(time.time()))
s=SnoperCrawler()
s.ReadLog()
for i in range(2,3):
    s.CrawOnePage(i)
    s.  WriteJSON()
