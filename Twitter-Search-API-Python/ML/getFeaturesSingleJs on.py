import findspark
import os
from nltk.sentiment.util import getPositiveWords
from nltk.sentiment.util import getNegativeWords

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.parse import urlparse

sid = SentimentIntensityAnalyzer()
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

URLdict=dict()
with open(  path.TweetJSONpath+"WOtURLs.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        #URLdict[sentence.split('   ')[0]]=int(sentence.split('   ')[1].replace('\n',''))
        urldata=json.loads(sentence)
        URLdict[urldata['url']]=urldata
def getWOT(urls):
    sums=[]
    if len(urls)==0:
        return 0
    for url in urls:
        if url in URLdict.keys():
            sums.append( URLdict[url]['wot'])
        else:
            sums.append(0)
    return float(sum(sums))/len(sums)
def getUrlNews(urls):
    for url in urls:
        if url in URLdict.keys():
           if URLdict[url]['type']=='News/Media':
               return 1
    return 0

def getUrlRank(urls):
    rank=[]
    for url in urls:
        if url in URLdict.keys():
             rank.append(URLdict[url]['rank'])
    if len(rank)==0:
        return 0
    return min(rank)

largecitylist=list()
with open(  path.datapath+"LargeCity.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        largecitylist.append(sentence.replace('\n',''))

def isInlargecity(city):
    if len(city)<2:
        return  False
    for ct in largecitylist:
        if ct in city:
            return True
    return False

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
    t = datetime.datetime.fromtimestamp((json.loads(jsontext)['created_at']/1000))
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
def containVia(V):
    Iword=['via','Via']
    for iword in Iword:
        if iword in V:
            return 1
    return 0
def containStock(V):
    Iword='$'

    if Iword in V:
        return 1
    return 0
def containSmile(V):
    Iword=[':->',':-)',';->',';-)']
    for iword in Iword:
        if iword in V:
            return 1
    return 0
def containSad(V):
    Iword=[':-<',':-(',';->',';-(']
    for iword in Iword:
        if iword in V:
            return 1
    return 0
def containI(V):
    Iword=['I ','I\'m','I\'ve','my ','My ','Mine ',' mine ','i\'m','i\'ve',' we ','We ']
    for iword in Iword:
        if iword in V:
            return 1
    return 0
def containHeShe(V):
    Iword=['He ',' he ','HE ','SHE ','She ',' she ','He\'s','She\'s','my ','My ','They ','they ','they\'re','They\'re','THEY ']
    for iword in Iword:
        if iword in V:
            return 1
    return 0
def PersentofCapital(V):
    Iword='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    counter=0
    for char in V:
        if char in Iword:
            counter+=1
    return counter/len(V)

def getNumChars(V):
    Iword=set()
    counter=0
    for char in V:
        Iword.add(char)
    return len(Iword)

def containU(V):
    Iword=['You ',' U ',' you ','your']
    for iword in Iword:
        if iword in V:
            return 1
    return 0

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
userdict=dict()
with open(path.USerJSONpath+'User_JSON.txt', mode='r')as Seenlist2:
        for line in Seenlist2:
            user=json.loads(line)
            userdict[user['user_id']]=user
def setTOdict(Toavg):
    retdict=dict()
    for toav in Toavg:
        retdict[toav[0]]=toav[1]
    return retdict

def getUserFromID(id):
    user = {
            'data-background-image': None,
            'user_id': id,
            'user_screen_name': None,
            'user_name': None,
            'followers_count': 0,
            'location':None,
            'friends_count':0,
            'favourites_count':0,
            'photos_count':0,
            'tweets_count':0,
            'Join_date':'1:01 AM - 1 Aug 2016',
            'Description':'',
            'hashtagsInDescription':list(),
            'menstionInDescription':list(),
            'urlsInDescription':list(),
            'url':None,
            'verified':False
        }
    try:
        return userdict[int(id)]
    except KeyError:
        user['user_id']=int(id)
        return user

datafolder=path.TweetJSONpath+'news/'
descriptionFile=path.TweetJSONpath+'descriptionNews.txt'
outputFile=path.Featurepath+'featuresNewsWOT.txt'
# datafolder=path.TweetJSONpath+'news/'
# descriptionFile=path.TweetJSONpath+'descriptionNews.txt'
# outputFile=path.Featurepath+'featuresNews.txt'

timeformate='%I:%M %p - %d %b %Y'
timetoday=datetime.datetime.strptime("10 7 2016",'%d %m %Y')
list_dirs = os.walk(datafolder)
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):#and title.replace(' ','_') in file):
            title=file.replace('_',' ').replace('.txt','')
            with open(descriptionFile,encoding='utf-8', mode='r')as Seenlist2:
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
            rootJSONMap=rootmap.map(lambda line2:(getTimefromJson(line2),json.loads(line2))).filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate)
            map3 =rootmap.map(lambda line:(getTimefromJson(line),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
            def tranto01(bool):
                            if bool:
                                return 1
                            else:
                                return 0

            maplargeCity=sc.parallelize(largecitylist)
            mapUsersLargeCity=rootJSONMap.map(lambda v1:( getUserFromID(v1[1]["user_id"])['location'],1)).filter(lambda v:(v[0]!='')).reduceByKey(lambda v1,v2:v1+v2).map(lambda v1:v1[0])#.sortByKey(True,1).collect()
            mapUsersLargeCitySet=mapUsersLargeCity.cartesian(maplargeCity).filter(lambda v1:(v1[0] is not None and v1[1] in v1[0])).map(lambda v:v[0]).collect()

            #print(type(timetoday))
            #TweetNum=map3.filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).map(lambda v1:[v1[0],v1[1]]).sortByKey(True,1).collect()
            maplenthofTweet=rootJSONMap.map(lambda v1:({'tweetid':v1[1]['tweet_id'],'features':{
                                                        'lenthofTweet':len(v1[1]['text']),
                                                        'PositiveScoer':sid.polarity_scores(v1[1]["text"])['compound'],
                                                        'NumPositiveWords':len(getPositiveWords(v1[1]["text"])),
                                                        'NumNegativeWords':len(getNegativeWords(v1[1]["text"])),
                                                        'numUrls':len(v1[1]["urls"]),
                                                        'WotScore':getWOT(v1[1]["extend_urls"]),
                                                        'ContainNEWS':getUrlNews(v1[1]["extend_urls"]),
                                                        'UrlRank':getUrlRank(v1[1]["extend_urls"]),
                                                        'Favorites':v1[1]['favorites'],
                                                        'Hashtag':len(v1[1]['hashtags']),
                                                        'Isretweet':tranto01(v1[1]['isretweet']),
                                                        'Retweets':v1[1]['retweets'],#10
                                                        'Contain_videos':tranto01(v1[1]['contain_videos']),
                                                        'Stock':containStock(v1[1]['text']),
                                                        'NumChar':getNumChars(v1[1]['text']),
                                                        'Capital':PersentofCapital(v1[1]['text']),
                                                        'Via':containVia(v1[1]['text']),
                                                        'I':containI(v1[1]['text']),
                                                        'Smile':containSmile(v1[1]['text']),
                                                        'Sad':containSad(v1[1]['text']),
                                                        'HeShe':containHeShe(v1[1]['text']),
                                                        'You':containU(v1[1]['text']),#20
                                                        'Menstion':len(v1[1]['menstion']),
                                                        'Question':containQuestion(v1[1]['text']),
                                                        'Exclamation':containexclamation(v1[1]['text']),
                                                        'QuestionExclamation':tranto01(containQuestion(v1[1]['text'])>1 or containexclamation(v1[1]['text'])>1),
                                                        'UserDescription':tranto01(len(getUserFromID(v1[1]["user_id"])['Description'])>0),
                                                        'Userverified':tranto01(getUserFromID(v1[1]["user_id"])['verified']),
                                                        'Userfollowers_count':getUserFromID(v1[1]["user_id"])['followers_count'],
                                                        'Userfriends_count':getUserFromID(v1[1]["user_id"])['friends_count'],
                                                        'Usertweets_count':getUserFromID(v1[1]["user_id"])['tweets_count'],
                                                        'UserrepitationScore':getrepitationScore(float(getUserFromID(v1[1]["user_id"])['followers_count']),getUserFromID(v1[1]["user_id"])['friends_count']),
                                                        'UserJoin_date':(timetoday-datetime.datetime.strptime(getUserFromID(v1[1]["user_id"])['Join_date'],timeformate)).days ,
                                                        'NumPhotos':v1[1]['contain_photos_number'],#32
                                                        'UserNumphoto':getUserFromID(v1[1]["user_id"])['photos_count'],
                                                        'UserIsInLargeCity':tranto01(getUserFromID(v1[1]["user_id"])['location'] in mapUsersLargeCitySet)},
                                                        'time':getHours(begindate,v1[0])}

                                            )).collect()

            maplenthofTweet={'eventID':mytweet['eventID'],'data':maplenthofTweet}

            with open(outputFile, mode='a') as writer:
                JSON=json.dumps(maplenthofTweet)
                writer.write(JSON + '\n')
