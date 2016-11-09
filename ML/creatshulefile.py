
import mypath as path
import json
import random
eventid=[]

with open(path.Featurepath+'descriptionRumors.txt',encoding='utf-8', mode='r')as Seenlist2:
    for line in Seenlist2:
        eventid.append(json.loads(line)['eventID'])


with open(path.Featurepath+'descriptionNews.txt',encoding='utf-8', mode='r')as Seenlist2:
    for line in Seenlist2:
        eventid.append(json.loads(line)['eventID'])


random.seed(0)
random.shuffle(eventid)

with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='w') as writer:
     writer.write(json.dumps(eventid))
