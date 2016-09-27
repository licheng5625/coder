import mypath as path
import json
import os
import featuresdecription
# outputFile=path.Featurepath+'featuresNewsTimeSeriorCreditMerged.txt'
# inputFile=path.Featurepath+'featuresNewsTimeSerior.txt'
# mergeFile=path.Featurepath+'featuresNewsTimeSeriorCredit.txt'
outputFile=path.Featurepath+'featuresRumorsTimeSeriorCreditMerged.txt'
inputFile=path.Featurepath+'featuresRumorsTimeSerior.txt'
mergeFile=path.Featurepath+'featuresRumorsTimeSeriorCredit.txt'

mergefeatures=['DebunkingWords']

#mergefeatures=featuresdecription.featureTypes['spikM']#['creditScore']




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
        newdeature=tweetslist[eventID]
        for feature in oldfeature.keys():
            mergeTweet=oldfeature[feature]
            for addfeatur in mergefeatures:
               # print(mergeTweet .keys())
                mergeTweet[addfeatur]=newdeature[feature][addfeatur]
        if eventID in counter:
            print(counter)
        counter.add(eventID)
        with open(outputFile,encoding='utf-8', mode='a')as Seenlist3:
                Seenlist3.write(json.dumps(data)+'\n')