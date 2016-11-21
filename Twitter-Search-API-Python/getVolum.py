import findspark
import os
from nltk.sentiment.util import getPositiveWords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.dates as mdates
import matplotlib

sid = SentimentIntensityAnalyzer()
os.environ['LC_ALL'] = 'en_US.UTF-8'

#matplotlib.use('Agg')

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

    fmt="%Y-%m-%d-%H"
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
def getHours(time1,time2):
   return int((time2-time1).days*24+(time2-time1).seconds/3600)
def containI(V):
    Iword=['I ','I\'m','I\'ve','my ','My']
    for iword in Iword:
        if iword in V:
            return True
    return False
def containQuestion(V):
    count=0
    for char in V:
        if char=='?':
            count=count+1
    return  count

def containexclamation(V):
    count=0
    for char in V:
        if char=='!':
            count=count+1
    return  count

def getReputationScore(follower,following):
    if following == 0:
        return 0
    return  float(follower)/float(following)


mytweet=None


def getrepitationScore(following,follower):
    if follower is 0:
        return 0
    return float(following)/follower


def addfrombefore(datalist):
    for i in range(1,len(datalist)):
            datalist[i][1]+=datalist[i-1][1]
    return datalist
    #return json.loads(jsontext)["items_html"]


checklist=list()

timeformate='%I:%M %p - %d %b %Y'
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/news/')
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):#and title.replace(' ','_') in file):
            title=file.replace('_',' ').replace('.txt','')
            if ('muni' not in title):
                continue
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/descriptionNews.txt', mode='r')as Seenlist2:
                for line in Seenlist2:
                    data=json.loads(line)
                    if data['tweetsQueryInGoogle'] ==title:
                        mytweet=data
            print(title)
            datapath=root+file
            rootmap =sc.textFile(datapath)
            enddate=datetime.datetime.strptime(mytweet['endDate'],"%Y-%m-%d-%H")
            begindate=datetime.datetime.strptime(mytweet['begindenDate'],"%Y-%m-%d-%H")

            def getAvg(Num,Toavg):
                Volume = [0 for n in range(getHours(begindate,enddate)+1)]
                Volume2 = [0 for n in range(getHours(begindate,enddate)+1)]
                for nu in Num:
                    Volume[nu[0]]=nu[1]
                for x in range(len(Volume)):
                    for i in range(x):
                        Volume[x]=Volume[i]+ Volume[x]
                for nu in Toavg:
                    Volume2[nu[0]]=nu[1]
                for x in range(len(Volume)):
                    for i in range(x):
                        Volume2[x]=Volume2[i]+ Volume2[x]
                for x in range(len(Volume)):
                    Volume2[x]=float(Volume2[x])/Volume[x]
                return Volume2
            # rootJSONMap=rootmap.map(lambda line2:(getTimefromJson(line2),1)).filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
            rootJSONMap=rootmap.map(lambda line2:(getTimefromJson(line2),1)).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)

            # map3 =rootmap.map(lambda line:(getTimefromJson(line),1)).reduceByKey(lambda v1,v2:v1+v2)
            #TweetNum=map3.filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2)
            # output=dict()
            # output['title']=title
            # output['volume']=TweetNum.map(lambda v:v[1]).collect()
            # with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/vulomnews.txt', mode='a') as writer:
            #     JSON=json.dumps(output)
            #     writer.write(JSON + '\n')


            TweetVolumeSUM = [0 for n in range(getHours(begindate,enddate))]
            TweetVolume = [0 for n in range(getHours(begindate,enddate))]

            dates=rootJSONMap.map(lambda v:v[0]).collect()
            times=rootJSONMap.map(lambda v:v[1]).collect()
            outputs=rootJSONMap.collect()
            for x  in range(len(TweetVolumeSUM)):
                for output in outputs:
                    if output[0]<=x:
                        TweetVolumeSUM[x]+=output[1]
                    if output[0]==x:
                        TweetVolume[x]+=output[1]
            Volstr='['
            for tweetvo in TweetVolume:
                Volstr+=str(tweetvo)+','
            print(Volstr)
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data.txt', mode='w') as writer:
                #for vol in TweetVolume:
                writer.write(str(TweetVolumeSUM)+'\n')



##画图表
            # import matplotlib.pyplot as plt
            # plt.plot(dates, times)
            # plt.xlabel('Hours')
            # plt.ylabel('#Tweets')
            # plt.title(title)
            # plt.savefig('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/picture/Rumors/'+title+'2.png')
            # plt.close('all')