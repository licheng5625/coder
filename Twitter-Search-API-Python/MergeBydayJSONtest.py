import findspark
import os
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
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
    t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
    fmt="%Y-%m-%d-%H"
    # return  t.strftime(fmt)
    return t
def getTimeStrfromTime(t):
    # t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
    fmt="%Y-%m-%d"
    return  t.strftime(fmt)
    # return t

def getUserfromJson(jsontext):
    return  json.loads(jsontext)['user_id']

def getMax(a,b):
    if b is None:
        return a
    else:
        return b

def getThrowhold(sum):
    if sum/100<10:
        return 10
    else :
        return sum/100
    #return json.loads(jsontext)["items_html"]
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/news/')
for root, dirs, files in list_dirs:
    for file in files:
        if ('munich' not in file):
            continue
        if ('.txt'in file):
            title=file.replace('_',' ').replace('.txt','')
            mytweet=None
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/descriptionNews.txt', mode='r')as Seenlist2:
                for line in Seenlist2:
                    data=json.loads(line)
                    if data['tweetsQueryInGoogle'] ==title:
                        mytweet=data
            if mytweet is None:
                break
            datapath=root+file
            print(datapath)
            # begindate=datetime.datetime.strptime(mytweet['begindenDate'],"%Y-%m-%d-%H")
            # snpesbegin=begindate-datetime.timedelta(3)
            # snpesend=begindate+datetime.timedelta(3)
            dates=[]
            # for i in range(148):
            #     dates.append(getTimeStrfromTime(snpesbegin+datetime.timedelta(seconds=i*3600)))
            # maple=sc.parallelize(dates).map(lambda line:(line,0))
            # print(maple.collect())
            rootmap =sc.textFile(datapath)
            map3 =rootmap.map(lambda line:(getTimefromJson(line),1))#.filter( lambda v1:(v1[0]>=snpesbegin and v1[0]<=snpesend))#.cartesian(maple)#.sortByKey(True,1)
            map3=map3.map(lambda v1:(getTimeStrfromTime(v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
            # map3=maple.leftOuterJoin(map3).map(lambda line:(line[0],getMax(line[1][0],line[1][1]))).sortByKey(True,1)
            # print(map3.collect())
            dates=map3.map(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")).collect()
            times=map3.map(lambda v1:v1[1]).collect()

            years = mdates.YearLocator()   # every year
            months = mdates.MonthLocator( )  # every month
            #days = mdates.DayLocator(interval=3 )  # every month
            days = mdates.HourLocator(interval=1 )  # every month

            hourssFmt = mdates.DateFormatter('%Y-%m-%d-%H')

            daysFmt = mdates.DateFormatter('%Y-%m-%d')
            yearsFmt = mdates.DateFormatter('%Y-%m')

            fig, ax = plt.subplots()
            dates = matplotlib.dates.date2num(dates)

            ax.plot_date(dates, times,'-' )

            #ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(daysFmt)
            ax.xaxis.set_minor_locator(months)
            ax.autoscale_view()

            def price(x):
                return   x
            ax.fmt_xdata = daysFmt
            ax.fmt_ydata = price
            ax.grid(True)

            fig.autofmt_xdate()
            plt.xlabel('Date')
            plt.ylabel('#Tweets')

            plt.show()






##画图表

