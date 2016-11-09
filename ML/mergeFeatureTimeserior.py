import mypath as path
import json
import os
import featuresdecription
# outputFile=path.Featurepath+'featuresRumorsTimeSerior130.txt'
# inputFile=path.Featurepath+'featuresRumorsTimeSerior130old.txt'
# mergeFile=path.Featurepath+'featuresRumorsTimeSeriorTwe.txt'
outputFile=path.Featurepath+'featuresNewsTimeSerior130.txt'
inputFile=path.Featurepath+'featuresNewsTimeSerior130old.txt'
mergeFile=path.Featurepath+'featuresNewsTimeSeriorWe.txt'

# mergefeatures=['beta','gamma','B','b','l','e','p','Pp','Pa','Ps','Qp','Qa','Qs']
# mergefeatures=['B','b','l','e','p','rho','SEIZIndex']
#mergefeatures=featuresdecription.featureTypes['spikM']#['creditScore']

mergefeatures=['UserTweetsPerDays']


tweetslist={}


with open(mergeFile,encoding='utf-8', mode='r')as Seenlist2:
    for line in Seenlist2:
       data=json.loads(line)
       eventID=data['eventID']
       features=data['features']
       tweetslist[eventID]=features

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
        oldfeature=data['features']
        try:
            newdeature=tweetslist[eventID]
        except:
            continue
        for feature in oldfeature.keys():
            mergeTweet=oldfeature[feature]
            for addfeatur in mergefeatures:
                mergeTweet[addfeatur]=newdeature[feature][addfeatur]
            # p=newdeature[feature]['p']
            # B=newdeature[feature]['B']
            # b=newdeature[feature]['b']
            # l=newdeature[feature]['l']
            # e=newdeature[feature]['e']
            # mergeTweet['SEIZIndex']=((1-p)*B+(1-l)*b)/(p+e+1)
        if eventID in counter:
            print(counter)
        counter.add(eventID)
        with open(outputFile,encoding='utf-8', mode='a')as Seenlist3:
                Seenlist3.write(json.dumps(data)+'\n')