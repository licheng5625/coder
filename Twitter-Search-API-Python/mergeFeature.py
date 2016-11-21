import mypath as path
import json
import featuresdecription
import os
#datafolder=path.TweetJSONpath+'news/'
outputFile=path.Featurepath+'featuresRumorscredt.txt'
inputFile=path.Featurepath+'featuresRumors.txt'
mergeFile=path.Featurepath+'tweetRNN.txt'
outputFile=path.Featurepath+'featuresnewsmerge.txt'
inputFile=path.Featurepath+'featuresNews.txt'
mergeFile=path.Featurepath+'tweetRNN.txt'

mergefeatures=["creditScore"]
#mergefeatures=featuresdecription.featureTypes['spikM']#['creditScore']
#mergefeatures=["Userfollowers_count", "Userfriends_count", "UserNumphoto", "Userverified", "UserJoin_date", "UserDescription", "NumPhotos", "UserIsInLargeCity", "Usertweets_count", "UserrepitationScore" ]
with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
    indeslixt=json.loads(writer.read())


tweetslist={}

with open(mergeFile,encoding='utf-8', mode='r')as Seenlist2:
   tweets=json.loads(Seenlist2.read())
   for tweet in tweets.keys():
        tweetslist[tweet]=int(tweets[tweet])



# with open(mergeFile,encoding='utf-8', mode='r')as Seenlist2:
#     for line in Seenlist2:
#        data=json.loads(line)
#        eventID=data['eventID']
#        tweets=data['data']
#        for tweet in tweets:
#             tweetslist[tweet['tweetid']]=tweet['features']
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
        if eventID not in indeslixt:
            continue
        print(eventID)
        # if eventID <=405:
        #     continue
        tweets=data['data']
        for tweet in tweets:
            for featur in mergefeatures:
                # tweet['features'][featur]=tweetslist[tweet['tweetid']][featur]
                # print(tweet['features'] )
                # print(tweetslist[tweet['tweetid']])
                try:
                    tweet['features'][featur]=tweetslist[tweet['tweetid']]
                except KeyError:
                    tweet['features'][featur]=tweetslist[str(tweet['tweetid'])]

        if eventID in counter:
            print(counter)
        counter.add(eventID)
        with open(outputFile,encoding='utf-8', mode='a')as Seenlist3:
                Seenlist3.write(json.dumps(data)+'\n')