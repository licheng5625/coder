import json
import mypath as path
listofrumor=[]

with open(path.Featurepath+'featuresrumorsTextlable.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

tweetid={}
with open(path.Featurepath+'tweetRNN.txt', mode='r') as writer:
    for line in writer:
        tweetid=json.loads(line)


with open(path.Featurepath+'wronglabel.txt', encoding='utf-8',mode='w') as writer:
    with open(path.Featurepath+'truelabel.txt', encoding='utf-8',mode='w') as writer2:

        for event in listofrumor:
            writer.write("eventID: "+str(event['eventID'])+'\n')
            writer2.write("eventID: "+str(event['eventID'])+'\n')
            try:
                for tweet in event['data']:
                    if tweetid[tweet['tweetid']] != "1":
                            writer.write(tweet['features']+'\n')
                    else:
                            writer2.write(tweet['features']+'\n')
            except KeyError:
                for tweet in event['data']:
                    if tweetid[str(tweet['tweetid'])] != "1":
                            writer.write(tweet['features']+'\n')
                    else:
                            writer2.write(tweet['features']+'\n')

