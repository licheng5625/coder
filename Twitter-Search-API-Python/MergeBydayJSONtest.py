import findspark
import os
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
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
with open(  path.datapath+"RumorsLIST.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        checkedtitle=sentence.split("@,@")[1].replace('\n','')
        rumorlist[checkedtitle]=sentence.split("@,@")[0]



def getTimefromJson(jsontext):
    t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
    fmt="%Y-%m-%d"
    return  t.strftime(fmt)

def getUserfromJson(jsontext):
    return  json.loads(jsontext)['user_id']


def getThrowhold(sum):
    if sum/100<10:
        return 10
    else :
        return sum/100

    #return json.loads(jsontext)["items_html"]
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/rumors/')
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):
            datapath=root+file
            print(datapath)
            rootmap =sc.textFile(datapath)
            map3 =rootmap.map(lambda line:(getTimefromJson(line),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)

            dates=map3.map(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")).collect()
            times=map3.map(lambda v1:v1[1]).collect()
            years = mdates.YearLocator()   # every year
            months = mdates.MonthLocator( )  # every month
            days = mdates.DayLocator(interval=3 )  # every month
            daysFmt = mdates.DateFormatter('%Y-%m-%d')
            yearsFmt = mdates.DateFormatter('%Y-%m')

            fig, ax = plt.subplots()
            dates = matplotlib.dates.date2num(dates)

            ax.plot_date(dates, times,'-' )

            #ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(daysFmt)
            ax.xaxis.set_minor_locator(days)
            ax.autoscale_view()

            def price(x):
                return   x
            ax.fmt_xdata = daysFmt
            ax.fmt_ydata = price
            ax.grid(True)

            fig.autofmt_xdate()
            plt.show()






##画图表

