import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.parse import urlparse

sid = SentimentIntensityAnalyzer()
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import json
import path

import datetime

import LMtext

def addfrombefore(datalist):
    for i in range(1,len(datalist)):
            datalist[i][1]+=datalist[i-1][1]
    return datalist
    #return json.loads(jsontext)["items_html"]

#
datafolder=path.TweetJSONpath+'news/'
descriptionFile=path.TweetJSONpath+'descriptionNews.txt'
outputFile=path.Featurepath+'featuresNewsTimeSeriorCredit.txt'
Singlefeautrefile=path.Featurepath+'featuresNews.txt'


# datafolder=path.TweetJSONpath+'rumors/'
# descriptionFile=path.TweetJSONpath+'descriptionRumors.txt'
# outputFile=path.Featurepath+'featuresRumorsTimeSeriorCredit.txt'
# Singlefeautrefile=path.Featurepath+'featuresRumors.txt'

isrumor=0
eventdict={}

with open(Singlefeautrefile, mode='r') as reader:
    for line in reader:
        JSON=json.loads(line)
        eventdict[JSON['eventID']]=JSON['data']

try:
    os.remove(outputFile)
except Exception:
    pass

totallnum=[]
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
            eventID=mytweet['eventID']
            event=eventdict[eventID]
            outputfeature={'eventID':eventID,'isrumor':isrumor}
            tweetlist=[[] for n in range(49)]
            #print(len(event))
            volumeperHour=[0 for n in range(49)]
            for tweet in event:
                for i in range(49):
                    if tweet['time']== i:
                        volumeperHour[i]+=1
            for tweet in event:
                for i in range(49):
                    if tweet['time']<= i:
                        #print(str(tweet['time'])+'add to '+str(i))

                        tweetlist[i].append(tweet['features'])
            totallnum.append(len(tweetlist[48]))
            print(len(tweetlist[48]))
            outputfeature['features']={}
            for i in range(49):
                volume=len(tweetlist[i])
                Userfollowers_count=0      #0
                PositiveScoer=0            #1
                Smile=0                    #2
                UserJoin_date=0            #3
                NumPositiveWords=0         #4
                You=0                      #5
                numUrls=0                  #6
                NumNegativeWords=0         #7
                UserDescription=0          #8
                Retweets=0                 #9
                Hashtag=0                  #10
                Capital=0                  #11
                Question=0                 #12
                Stock=0                    #13
                WotScore=0                 #14
                Contain_videos=0             #15
                HeShe=0                     #16
                I=0                         #17
                UserIsInLargeCity=0        #18
                UserNumphoto=0              #19
                Exclamation=0               #20
                QuestionExclamation=0        #21
                Sad=0                    #22
                Usertweets_count=0             #23
                UserrepitationScore=0       #24
                Userverified=0            #25
                Menstion=0              #26
                UrlRank=0               #27
                Userfriends_count=0     #28
                NumPhotos=0             #29
                NumChar=0               #30
                Via=0                   #31
                Favorites=0             #32
                lenthofTweet=0          #33
                ContainNEWS=0           #34
                Isretweet=0             #35
                creditScore=0
                UrlRankIn5000=0

                features={}
                outputfeature['features']["F"+str(i)]=features
                #features['Ps'],features['Qp'],features['Qs']=LMtext.fittoSpikeM(volumeperHour[:i])
                for tweet in tweetlist[i]:
                    # Userfollowers_count+=tweet['Userfollowers_count']
                    # PositiveScoer+=tweet['PositiveScoer']
                    # Smile+=tweet['Smile']
                    # UserJoin_date+=tweet['UserJoin_date']
                    # NumPositiveWords+=tweet['NumPositiveWords']
                    # You+=tweet['You']
                    # numUrls+=tweet['numUrls']
                    # NumNegativeWords+=tweet['NumNegativeWords']
                    # UserDescription+=tweet['UserDescription']
                    # Retweets+=tweet['Retweets']
                    # Hashtag+=tweet['Hashtag']
                    # Capital+=tweet['Capital']
                    # Stock+=tweet['Stock']
                    # WotScore+=tweet['WotScore']
                    # Contain_videos+=tweet['Contain_videos']
                    # HeShe+=tweet['HeShe']
                    # I+=tweet['I']
                    # UserIsInLargeCity+=tweet['UserIsInLargeCity']
                    # UserNumphoto+=tweet['UserNumphoto']
                    # Exclamation+=tweet['Exclamation']
                    # Question+=tweet['Question']
                    # QuestionExclamation+=tweet['QuestionExclamation']
                    # Sad+=tweet['Sad']
                    # Usertweets_count+=tweet['Usertweets_count']
                    # UserrepitationScore+=tweet['UserrepitationScore']
                    # Userverified+=tweet['Userverified']
                    # Menstion+=tweet['Menstion']
                    # UrlRank+=tweet['UrlRank']
                      UrlRankIn5000+=tweet['UrlRankIn5000']
                    # Userfriends_count+=tweet['Userfriends_count']
                    # NumPhotos+=tweet['NumPhotos']
                    # NumChar+=tweet['NumChar']
                    # Via+=tweet['Via']
                    # Favorites+=tweet['Favorites']
                    # lenthofTweet+=tweet['lenthofTweet']
                    # ContainNEWS+=tweet['ContainNEWS']
                    # Isretweet+=tweet['Isretweet']
                    # creditScore+=tweet['creditScore']



                # features['Userfollowers_count']=Userfollowers_count/float(volume)
                # features['PositiveScoer']=PositiveScoer/float(volume)
                # features['Smile']=Smile/float(volume)
                # features['UserJoin_date']=UserJoin_date/float(volume)
                # features['NumPositiveWords']=NumPositiveWords/float(volume)
                # features['You']=You/float(volume)
                features['UrlRankIn5000']=UrlRankIn5000/float(volume)

                # if numUrls!=0:
                #     features['WotScore']=WotScore/float(numUrls)
                #     features['UrlRank']=UrlRank/float(numUrls)
                #     features['ContainNEWS']=ContainNEWS/float(numUrls)
                # else:
                #     features['WotScore']=0
                #     features['UrlRank']=0
                #     features['ContainNEWS']=0
                # features['numUrls']=numUrls/float(volume)
                # features['NumNegativeWords']=NumNegativeWords/float(volume)
                # features['UserDescription']=UserDescription/float(volume)
                # features['Retweets']=Retweets/float(volume)
                # features['Hashtag']=Hashtag/float(volume)
                # features['Capital']=Capital/float(volume)
                # features['Stock']=Stock/float(volume)
                # features['Contain_videos']=Contain_videos/float(volume)
                # features['HeShe']=HeShe/float(volume)
                # features['I']=I/float(volume)
                # features['UserIsInLargeCity']=UserIsInLargeCity/float(volume)
                # features['UserNumphoto']=UserNumphoto/float(volume)
                # features['Exclamation']=Exclamation/float(volume)
                # features['QuestionExclamation']=QuestionExclamation/float(volume)
                # features['Usertweets_count']=Usertweets_count/float(volume)
                # features['UserrepitationScore']=UserrepitationScore/float(volume)
                # features['Userverified']=Userverified/float(volume)
                # features['Menstion']=Menstion/float(volume)
                # features['Userfriends_count']=Userfriends_count/float(volume)
                # features['NumPhotos']=NumPhotos/float(volume)
                # features['NumChar']=NumChar/float(volume)
                # features['Via']=Via/float(volume)
                # features['Favorites']=Favorites/float(volume)
                # features['lenthofTweet']=lenthofTweet/float(volume)
                # features['Isretweet']=Isretweet/float(volume)
                # features['Sad']=Sad/float(volume)
                # features['Question']=Question/float(volume)
                # features['creditScore']=creditScore/float(volume)
                if (i!=0):
                    features={}
                    outputfeature['features']["S"+str(i)]=features
                    for feature in outputfeature['features']["F"+str(i)].keys():
                        features[feature]=outputfeature['features']["F"+str(i)][feature]-outputfeature['features']["F"+str(i-1)][feature]

                #print (str(volume)+'    '+str(sumLength)+' accuracy: %.2f' % (sumLength/float(volume)))







            with open(outputFile, mode='a') as writer:
                JSON=json.dumps(outputfeature)
                writer.write(JSON + '\n')
