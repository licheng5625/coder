import path
import json

outpuh=[]
with open(path.TweetJSONpath+'description.txt',encoding='utf-8', mode='r')as Seenlist2:
    counter=0
    for line in Seenlist2:
        data=json.loads(line)
        data['eventID']=3*100+counter
        counter+=1
        outpuh.append(data)
with open(path.TweetJSONpath+'descriptionRumors.txt',encoding='utf-8', mode='w')as Seenlist2:
    for out in outpuh:
        JSON=json.dumps(out)
        Seenlist2.write(JSON+'\n')