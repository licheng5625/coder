import findspark
import os
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import json
import path
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
with open(  path.datapath+"NewsLISTforBBC.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        checkedtitle=sentence.split("@,@")[1].replace('\n','')
        rumorlist[checkedtitle]=sentence.split("@,@")[0]


def getTimefromJson(jsontext):
    t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))

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
    #return json.loads(jsontext)["items_html"]
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/newsBBC/')
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):
            datapath=root+file
            rootmap =sc.textFile(datapath)
            mytweet=dict()
            mytweet['tweetsQueryInGoogle']=file.replace('.txt','').replace('_',' ')
            mytweet['tweetsQuery']=rumorlist[file.replace('.txt','')]
            mytweet['tweetFile']=datapath
            #usermap=rootmap.map(lambda line:(getUserfromJson(line),(getTimefromJson(line),1)))
            #usermapreduce=usermap.map(lambda v1:(v1[0],v1[1][1])).reduceByKey(lambda v1,v2:v1+v2).sortBy(lambda x: x[1])
            #tweetidmap =rootmap.map(lambda line:(getTimefromJson(line),getIDfromJson(line))).sortByKey(True,1)
            map3=rootmap.map(lambda line:(getTimefromJson(line)))
            mapmergebyday =rootmap.map(lambda line:(getTimefromJson(line).strftime(fmt),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
            mapsum=mapmergebyday.map(lambda line:line[1]).sum()
            tweets=mapmergebyday.collect()
            #mytweet['tweets']=map3.collect()
            #mytweet['tweetsNum']=mapsum
            mytweet['maxTweetsInDay']=max(tweets,key=sortBytweet)[1]
            mytweet['maxTweetsDay']=max(tweets,key=sortBytweet)[0]
            #mytweet['userlist']=usermapreduce.collect()
            #throwhold =getThrowhold(mapsum)
            #begindate=datetime.datetime.strptime(map3.filter(lambda v1: v1[1]>throwhold).collect()[0][0] ,"%Y-%m-%d")
            enddate=datetime.datetime.strptime(mytweet['maxTweetsDay'],"%Y-%m-%d")+datetime.timedelta(1)
            begindate=enddate-datetime.timedelta(2)
            mapfiliterbyday=map3.filter(lambda v1:v1>=begindate).filter(lambda v1:v1<=enddate).sortBy(lambda x: x)
            mytweet['firstTweetTime']=mapfiliterbyday.collect()[0]
            begindate=mytweet['firstTweetTime']
            mytweet['firstTweetTime']=mytweet['firstTweetTime'].strftime("%Y-%m-%d-%H")
            enddate=begindate+datetime.timedelta(days=2)+datetime.timedelta(seconds=3600)
            mytweet['endDate']=enddate.strftime("%Y-%m-%d-%H")
            mytweet['begindenDate']= begindate.strftime("%Y-%m-%d-%H")
            #mapsum=map3.map(lambda line:line[1]).sum()
            #mytweet['tweetsInPeekTime']=map3.collect()
            #mytweet['tweetsNumInPeekTime']=mapsum
            #tweetidmap.filter(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")>=begindate).filter(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")<=enddate)

            #usermap=usermap.filter(lambda v1:datetime.datetime.strptime(v1[1][0],"%Y-%m-%d")>=begindate).filter(lambda v1:datetime.datetime.strptime(v1[1][0],"%Y-%m-%d")<=enddate)
            #usermapreduce=usermap.map(lambda v1:(v1[0],v1[1][1])).reduceByKey(lambda v1,v2:v1+v2).sortBy(lambda x: x[1])
            #mytweet['userlistInPeekTime']=usermapreduce.collect()
            with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'descriptionNewsForBBC.txt', mode='a')as Seenlist2:
                JSON = json.dumps(mytweet, ensure_ascii=False)
                Seenlist2.write(JSON + '\n')





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
