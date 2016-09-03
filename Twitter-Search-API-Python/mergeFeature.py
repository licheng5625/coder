import path
import json
import os
#datafolder=path.TweetJSONpath+'news/'
outputFile=path.Featurepath+'featuresRumorsNumphoto2.txt'
inputFile=path.Featurepath+'featuresRumors.txt'
mergeFile=path.Featurepath+'featuresRumorsNumphoto.txt'
mergefeatures=['UrlRankIn5000']
#mergefeatures=["Userfollowers_count", "Userfriends_count", "UserNumphoto", "Userverified", "UserJoin_date", "UserDescription", "NumPhotos", "UserIsInLargeCity", "Usertweets_count", "UserrepitationScore" ]


tweetslist={}




with open(mergeFile,encoding='utf-8', mode='r')as Seenlist2:
    for line in Seenlist2:
       data=json.loads(line)
       eventID=data['eventID']
       tweets=data['data']
       for tweet in tweets:
            tweetslist[tweet['tweetid']]=tweet['features']
       #tweetslist=data
            #tweet['features']['creditScore']=int(tweetIDscore[tweet['tweetid']])
try:
    with open(outputFile,encoding='utf-8', mode='r')as Seenlist3:
        pass
    os.remove(outputFile)
except Exception:
    pass
with open(inputFile,encoding='utf-8', mode='r')as Seenlist2:
    counter=set()
    for line in Seenlist2:
        data=json.loads(line)
        eventID=data['eventID']
        print(eventID)
        tweets=data['data']
        for tweet in tweets:
            for featur in mergefeatures:
                tweet['features'][featur]=tweetslist[tweet['tweetid']][featur]
        if eventID in counter:
            print(counter)
        counter.add(eventID)
        with open(outputFile,encoding='utf-8', mode='a')as Seenlist3:
                Seenlist3.write(json.dumps(data)+'\n')