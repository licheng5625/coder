import findspark
import os
from nltk.sentiment.util import getPositiveWords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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

rumorlist=dict()
with open(  path.datapath+"RumorsLIST.txt",encoding="utf-8", mode='r') as Seenlist:
    for sentence in Seenlist:
        checkedtitle=sentence.split("@,@")[1].replace('\n','')
        rumorlist[checkedtitle]=sentence.split("@,@")[0]



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

checklist=list()
try:
    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data2.txt', mode='r') as writer:
            for line in writer:
                checklist.append(json.loads(line)['name'])
except FileNotFoundError:
    pass

timeformate='%I:%M %p - %d %b %Y'
timetoday=datetime.datetime.strptime("10 7 2016",'%d %m %Y')
list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_JSON/newsBBC/')
for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):#and title.replace(' ','_') in file):
            title=file.replace('_',' ').replace('.txt','')
            if (title in checklist):
                continue
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/descriptionNewsForBBC.txt', mode='r')as Seenlist2:
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
                Volume = [0 for n in range(49)]
                Volume2 = [ ]
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

            TweetNum=map3.filter(lambda v1:v1[0]>=begindate).filter(lambda v1:v1[0]<=enddate).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).map(lambda v1:[v1[0],v1[1]]).sortByKey(True,1).collect()
            print(TweetNum)
            maplenthofTweet=rootJSONMap.map(lambda v1:(getHours(begindate,v1[0]),len(v1[1]['text']))).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            print(maplenthofTweet)
            maplenthofTweet=getAvg(TweetNum,maplenthofTweet)

            mapPositiveScoer=rootJSONMap.map(lambda v1:(getHours(begindate,v1[0]),sid.polarity_scores(v1[1]["text"])['compound'])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapPositiveScoer=getAvg(TweetNum,mapPositiveScoer)

            mapNumPositive=rootJSONMap.filter(lambda v1:sid.polarity_scores(v1[1]["text"])['compound']>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapNumPositive=getAvg(TweetNum,mapNumPositive)

            mapPositiveWord=rootJSONMap.map(lambda v1:(getHours(begindate,v1[0]),len(getPositiveWords(v1[1]["text"])))).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapPositiveWord=getAvg(TweetNum,mapPositiveWord)

            mapURL=rootJSONMap.filter(lambda v1:len(v1[1]["urls"])>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapURL=getAvg(TweetNum,mapURL)


            mapHashtag=rootJSONMap.filter(lambda v1:len(v1[1]['hashtags'])>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapHashtag=getAvg(TweetNum,mapHashtag)


            mapI=rootJSONMap.filter(lambda v1:containI(v1[1]['text'])).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapI=getAvg(TweetNum,mapI)

            mapMention=rootJSONMap.filter(lambda v1:len(v1[1]['menstion'])>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapMention=getAvg(TweetNum,mapMention)

            mapQuestion=rootJSONMap.filter(lambda v1:containQuestion(v1[1]['text'])>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapQuestion=getAvg(TweetNum,mapQuestion)

            mapExclamation=rootJSONMap.filter(lambda v1:containexclamation(v1[1]['text'])>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapExclamation=getAvg(TweetNum,mapExclamation)

            mapQuestionExclamation=rootJSONMap.filter(lambda v1:(containQuestion(v1[1]['text'])>1 or containexclamation(v1[1]['text'])>1)).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapQuestionExclamation=getAvg(TweetNum,mapQuestionExclamation)

            mapUser=rootJSONMap.map(lambda v1:(v1[0],getUserFromID(v1[1]["user_id"])))
            mapUserNum=rootJSONMap.map(lambda v1:(v1[0],v1[1]["user_id"])).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()


            mapUserDescription=mapUser.filter(lambda v1:len(v1[1]['Description'])!=0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserDescription=getAvg(mapUserNum,mapUserDescription)


            mapUserPhoto=mapUser.filter(lambda v1:v1[1]['photos_count']>0).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserPhoto=getAvg(mapUserNum,mapUserPhoto)


            maplargeCity=sc.parallelize(largecitylist)
            mapUsersLargeCity=mapUser.map(lambda v1:(v1[1]['location'],1)).filter(lambda v:(v[0]!='')).reduceByKey(lambda v1,v2:v1+v2).map(lambda v1:v1[0])#.sortByKey(True,1).collect()
            mapUsersLargeCitySet=mapUsersLargeCity.cartesian(maplargeCity).filter(lambda v1:(v1[0] is not None and v1[1] in v1[0])).map(lambda v:v[0]).collect()
            mapUsersInLargeCity=mapUser.filter(lambda v1:v1[1]['location'] in mapUsersLargeCitySet).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUsersInLargeCity=getAvg(mapUserNum,mapUsersInLargeCity)



            mapUserVerified=mapUser.filter(lambda v1:v1[1]['verified']).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserVerified=getAvg(mapUserNum,mapUserVerified)

            mapUserFollower=mapUser.map(lambda v1:(v1[0],v1[1]['followers_count'])).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserFollower=getAvg(mapUserNum,mapUserFollower)


            mapUserFollowing=mapUser.map(lambda v1:(v1[0],v1[1]['friends_count'])).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserFollowing=getAvg(mapUserNum,mapUserFollowing)


            mapUserReputationScore=mapUser.map(lambda v1:(v1[0],getrepitationScore(float(v1[1]['followers_count']),v1[1]['friends_count']))).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserReputationScore=getAvg(mapUserNum,mapUserReputationScore)


            mapUserPost=mapUser.map(lambda v1:(v1[0],v1[1]['tweets_count'])).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserPost=getAvg(mapUserNum,mapUserPost)

            #print(mapUser.filter(lambda v1:( (v1[1]['Join_date'])is None)).sortByKey(True,1).collect())
            mapUserResistation=mapUser.map(lambda v1:(v1[0],(timetoday-datetime.datetime.strptime(v1[1]['Join_date'],timeformate)).days)).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapUserResistation=getAvg(mapUserNum,mapUserResistation)


            mapVedio=rootJSONMap.filter(lambda v1:v1[1]['contain_videos']).map(lambda v1:(getHours(begindate,v1[0]),1)).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            mapVedio=getAvg(TweetNum,mapVedio)

            # mapUserFollower=mapUser.map(lambda v1:(v1[0],getReputationScore(v1[1]['followers_count'],v1[1]['friends_count']))).map(lambda v1:(getHours(begindate,v1[0]),v1[1])).reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1).collect()
            # mapUserFollower=getAvg(mapUserNum,mapUserFollower)
            #mapUserNum=setTOdict(mapUserNum)


            output=dict()
            output['name']=title
            output['maplenthofTweet']=maplenthofTweet
            output['mapPositiveScoer']=mapPositiveScoer
            output['mapNumPositive']=mapNumPositive
            output['mapPositiveWord']=mapPositiveWord
            output['mapURL']=mapURL
            output['mapHashtag']=mapHashtag
            output['mapI']=mapI
            output['mapMention']=mapMention
            output['mapQuestion']=mapQuestion
            output['mapExclamation']=mapExclamation
            output['mapQuestionExclamation']=mapQuestionExclamation
            output['mapUserDescription']=mapUserDescription
            output['mapUserPhoto']=mapUserPhoto
            output['mapUsersInLargeCity']=mapUsersInLargeCity
            output['mapUserFollower']=mapUserFollower
            output['mapUserFollowing']=mapUserFollowing
            output['mapUserPost']=mapUserPost
            output['mapUserResistation']=mapUserResistation
            output['mapUserReputationScore']=mapUserReputationScore
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/dataBBC.txt', mode='a') as writer:
                JSON=json.dumps(output)
                writer.write(JSON + '\n')


            #TweetVolume = [0 for n in range(getHours(begindate,enddate))]
           # percentOfUrl = [0 for n in range(getHours(begindate,enddate))]

            # for data in TweetNum:
            #      TweetVolume[data[0]]=TweetVolume[data[0]]+  data[1]
            # with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data.txt', mode='w') as writer:
            #     for vol in TweetVolume:
            #         writer.write(str(vol)+'\n')


##画图表

#dates=map3.map(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m-%d")).sortByKey(True,1).collect()
#times=map3.map(lambda v1:v1[1]).sortByKey(True,1).collect()
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
