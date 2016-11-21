import findspark
import os
import http.client
import urllib.parse

os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import json
import mypath as path
findspark.init(spark_home='/Applications/spark-1.6.1')

from pyspark import SparkContext, SparkConf

import datetime


def getNum(rdd,word):#return the sum up
    return rdd.filter(lambda v1:"apple" in v1[0]).map(lambda v1: v1[1]).sum()


def filtermap(word,vector):
    newve=list()
    for se in vector:
        if word in se[0]:
            newve.append(se)
    return newve
def merge(v1,v2):
    print (v1)
    print (v2)
    if(v1 is None) and v2 is None:
        return v1
    if (v1 is None):
        return v2
    if (v2 is None):
        return v1
    else:
        return (v1[0],v1[1]+v2[1])
conf = SparkConf().setAppName("Spark Count")
sc = SparkContext(conf=conf)

def sortBytweet(a):
    return a[1]


class TwitterDescribtor:
    tweetFile =str()
    tweetsNum=0
    tweetsNumInPeekTime=0
    tweets=list()
    tweetsInPeekTime=list()
    maxTweetsInDay=0
    maxTweetsDay=str()
    begindenDate=str()
    endDate=str()
    userlist=list()
    userlistInPeekTime=list()
    tweetsQuery=str()
    tweetsQueryInGoogle=str()

rumorlist=dict()
with open(  path.datapath+"RumorsLIST.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        checkedtitle=sentence.split("@,@")[1].replace('\n','')
        rumorlist[checkedtitle]=sentence.split("@,@")[0]


def getTimefromJson(jsontext):
    try:
        t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
    except:
        timetext=json.loads(jsontext)['created_at']
        timetext=timetext.replace(' 24:',' 23:')
        t = datetime.datetime.strptime(timetext,'%a %b %d %H:%M:%S +0000 %Y')

    return  t#.strftime(fmt)


def getUserfromJson(jsontext):
    return  json.loads(jsontext)['user_id']
def getIDfromJson(jsontext):
    return  json.loads(jsontext)['tweet_id']

def getThrowhold(sum):
    if sum/100<10:
        return 10
    else :
        return sum/100
fmt="%Y-%m-%d"
userlist=dict()
    #return json.loads(jsontext)["items_html"]
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/news/')
countnum=0
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):
            if 'mun' not in file:
                continue
            countnum=countnum+1
            print(countnum)
            datapath=root+file
            mytweet=None
            title=file.replace('.txt','')
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/descriptionNews.txt', mode='r')as Seenlist2:
                for line in Seenlist2:
                    data=json.loads(line)
                    if data['tweetsQueryInGoogle'] ==title:
                        mytweet=data
            if mytweet==None:
                continue
            print(file)
            print(data['tweetsQueryInGoogle'])

            rootmap =sc.textFile(datapath)


            enddate=datetime.datetime.strptime(mytweet['endDate'],"%Y-%m-%d-%H")
            begindate=datetime.datetime.strptime(mytweet['begindenDate'],"%Y-%m-%d-%H")


            rootJSONMap=rootmap.map(lambda line2:(getTimefromJson(line2),json.loads(line2))).filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate)
            rootJSONMap=rootJSONMap.map(lambda line:(line[1]['user_screen_name'],line[1]['user_id']))
            for usr in rootJSONMap.collect():
                userlist[usr[1]]=usr[0]

userdict=dict()
usersimple={}
with open(path.USerJSONpath+'User_JSON.txt', mode='r')as Seenlist2:
        for line in Seenlist2:
            user=json.loads(line)
            userdict[user['user_id']]=user


# with open(path.USerJSONpath+'simple_News_UserJson.txt', mode='r')as Seenlist2:
#         for line in Seenlist2:
#             user=json.loads(line)
#             usersimple[int(user['user_id'])]=user
#             # print(int(user['user_id']))
#             # print(12564162 in usersimple.keys())
#
# with open(path.USerJSONpath+'simple_News_UserJson2.txt', mode='r')as Seenlist3:
#         for line in Seenlist3:
#             user=json.loads(line)
#             usersimple[int(user['user_id'])]=user
            #print(12564162 in usersimple.keys())


# with open('/Users/licheng5625/Downloads/simple_News_UserJson.txt', mode='r')as Seenlist4:
#         for line in Seenlist4:
#             user=json.loads(line)
#             usersimple[int(user['user_id'])]=user
            #print(12564162 in usersimple.keys())

#
# with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/User_JSON/simple_News_UserJson.txt', mode='r')as Seenlist21:
#         for line in Seenlist21:
#             user=json.loads(line)
#             usersimple[int(user['user_id'])]=user

with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'usersnews.txt', mode='w')as Seenlist22:
    for user in userlist.keys():
        # if int(user) ==744163359793217536:
        #     print(user)
        #     print(int(user) in userdict.keys())
        if int(user) ==12564162:
            print(12564162 in usersimple.keys())

        if (int(user) not in userdict.keys() ) and (  int(user) !=2243030700):#and  (int(user) not in usersimple.keys()):
            #Seenlist22.write(str(user)+'	'+usersimple[int(user)]['screen_name']+'\n')
            Seenlist22.write(str(user)+'\n')
            #Seenlist22.write(str(user)+'\n')



##画图表

#dates=map3.map(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")).collect()
#times=map3.map(lambda v1:v1[1]).collect()
#years = mdates.YearLocator()   # every year
# months = mdates.MonthLocator(interval=4)  # every month
# daysFmt = mdates.DateFormatter('%Y-%m-%d')
# yearsFmt = mdates.DateFormatter('%Y-%m')
#
# fig, ax = plt.subplots()
# dates = matplotlib.dates.date2num(dates)
#
# ax.plot_date(dates, times,'-' )
#
# ax.xaxis.set_major_locator(months)
# ax.xaxis.set_major_formatter(yearsFmt)
# ax.xaxis.set_minor_locator(months)
# ax.autoscale_view()
#
# def price(x):
#     return   x
# ax.fmt_xdata = daysFmt
# ax.fmt_ydata = price
# ax.grid(True)
#
# fig.autofmt_xdate()
# plt.show()
