import findspark
import os
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



def getTimefromJson(jsontext):
    try:
        t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
    except TypeError:
        timetext=json.loads(jsontext)['created_at']
        timetext=timetext.replace(' 24:',' 23:')
        t = datetime.datetime.strptime(timetext,'%a %b %d %H:%M:%S +0000 %Y')

    fmt="%Y-%m-%d-%H"
    return  t#.strftime


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


# list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/news/')
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/rumors/')
rumorlist=dict()
with open(  path.datapath+"RumorsLIST.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        checkedtitle=sentence.split("@,@")[1].replace('\n','')
        rumorlist[checkedtitle]=sentence.split("@,@")[0]
maxtweet=0
mintweet=10000
sumtweet=[]
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):
            datapath=root+file
            rootmap =sc.textFile(datapath)
            mytweet=dict()
            mytweet['tweetsQueryInGoogle']=file.replace('.txt','').replace('_',' ')
            # mytweet['tweetsQuery']=rumorlist[file.replace('.txt','')]
            mytweet['tweetFile']=datapath
            map3=rootmap.map(lambda line:(getTimefromJson(line)))
            mapmergebyday =rootmap.map(lambda line:(getTimefromJson(line).strftime(fmt),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
            #mapsum=mapmergebyday.map(lambda line:line[1]).sum()
            tweets=mapmergebyday.collect()
            mytweet['maxTweetsInDay']=max(tweets,key=sortBytweet)[1]
            mytweet['maxTweetsDay']=max(tweets,key=sortBytweet)[0]
            mytweet['totalTweetVolum']=sum(mapmergebyday.map(lambda v1:v1[1]).collect())
            if mytweet['totalTweetVolum']<mintweet:
                mintweet=mytweet['totalTweetVolum']
            if mytweet['totalTweetVolum']>maxtweet:
                maxtweet=mytweet['totalTweetVolum']
            sumtweet.append(mytweet['totalTweetVolum'])
            # find the max pike of the event
            enddate=datetime.datetime.strptime(mytweet['maxTweetsDay'],"%Y-%m-%d")+datetime.timedelta(1)
            #begindate is the 48 hours(2 days) earlier
            begindate=enddate-datetime.timedelta(2)
            mapfiliterbyday=map3.filter(lambda v1:v1>=begindate).filter(lambda v1:v1<=enddate).sortBy(lambda x: x)
            mytweet['NumTweets']=len(mapfiliterbyday.collect() )

            mytweet['firstTweetTime']=mapfiliterbyday.collect()[0]
            # find the very first Tweet in this time range defind it as beginning time
            begindate=mytweet['firstTweetTime']
            mytweet['firstTweetTime']=mytweet['firstTweetTime'].strftime("%Y-%m-%d-%H")
            #  beginning time + 48 hours will the event time
            enddate=begindate+datetime.timedelta(days=2)+datetime.timedelta(seconds=3600)
            mytweet['endDate']=enddate.strftime("%Y-%m-%d-%H")
            # mytweet['eventID']=int(file.replace('.txt',''))

            mytweet['begindenDate']= begindate.strftime("%Y-%m-%d-%H")
            with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'descriptionnewrumor.txt', mode='a')as Seenlist2:
                JSON = json.dumps(mytweet, ensure_ascii=False)
                Seenlist2.write(JSON + '\n')

print(mintweet)
print(maxtweet)
print(sum(sumtweet))
print(sum(sumtweet)/len(sum))


