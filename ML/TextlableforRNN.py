from sklearn import svm
import numpy
import json
import random
import findspark
from random import shuffle
import os
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import json
import mypath as path
findspark.init(spark_home='/Applications/spark-1.6.1')

listofrumorevents={}
listofnewsevents={}
import  mypath as path
import featuresdecription
from pyspark import SparkContext, SparkConf

# with open(path.Featurepath+'featuresrumorsTextlable.txt', mode='r') as writer:
#     for line in writer:
#         JSON=json.loads(line)
#         listofrumorevents[JSON['eventID']]=JSON['data']
#
# with open(path.Featurepath+'featuresNewsTextlable.txt', mode='r') as writer:
#     for line in writer:
#         JSON=json.loads(line)
#         listofnewsevents[JSON['eventID']]=JSON['data']
conf = SparkConf().setAppName("Spark Count")
sc = SparkContext(conf=conf)



times=10
indeslixt=[]

with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
    indeslixt=json.loads(writer.read())

for time in range(times):
    if time!=2:
        continue
    lenofpiece=int(len(indeslixt)/times+0.5)
    selecttextevent=indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]
    outfile="train"+str(time)+'.txt'
    outfiletest="test"+str(time)+'.txt'

    rootmap =sc.textFile(path.Featurepath+'featuresrumorsTextlable.txt')

    rumormaptraintotal=rootmap.map(lambda v1:json.loads(v1))
    rumormaptrain= rumormaptraintotal.filter(lambda v:v['eventID'] not in selecttextevent).map(lambda v:v['data']).flatMap(lambda v:v).map(lambda v:v['features']).map(lambda v1:v1+',1').collect()
    rootmap2 =sc.textFile(path.Featurepath+'featuresNewsTextlable.txt')

    newsmaptraintotal=rootmap2.map(lambda v1:json.loads(v1))
    newsmaptrain=newsmaptraintotal.filter(lambda v:v['eventID'] not in selecttextevent).map(lambda v:v['data']).flatMap(lambda v:v).map(lambda v:v['features']).map(lambda v1:v1+',0').collect()

    newsmaptest=newsmaptraintotal.filter(lambda v:v['eventID'] in selecttextevent).map(lambda v:v['data']).flatMap(lambda v:v).map(lambda v:v['features']).map(lambda v1:v1+',0').collect()

    newsmaptrain+=rumormaptrain

    rumormaptest= rumormaptraintotal.filter(lambda v:v['eventID']  in selecttextevent).map(lambda v:v['data']).flatMap(lambda v:v).map(lambda v:v['features']).map(lambda v1:v1+',1').collect()
    rumormaptest+=newsmaptest

    #
    # for trainEventID in indeslixt:
    #     isRumor=0
    #     if trainEventID in listofrumorevents :
    #         event=listofrumorevents[trainEventID]
    #         isRumor=1
    #     else:
    #         event=listofnewsevents[trainEventID]
    #     if event == None:
    #         raise NameError(trainEventID)
    #     textdata=[]
    #     for tweet in event :
    #         if trainEventID not in selecttextevent :
    #             for tweet in event:
    #                 textdata.append(tweet['features']+str(isRumor))
    #         else:
    #             with open(path.Featurepath+'rnn/'+outfiletest,encoding='utf-8',mode='a') as writer:
    #                 tweet['type']=isRumor
    #                 writer.write(json.dumps(tweet)+'\n')
    shuffle(newsmaptrain)
    for data in newsmaptrain:
        with open(path.Featurepath+'rnn/'+outfile,encoding='utf-8',mode='a') as writer:
            writer.write(data.replace('\n','')+'\n')
    for data in rumormaptest:
        with open(path.Featurepath+'rnn/'+outfiletest,encoding='utf-8',mode='a') as writer:
            writer.write(data.replace('\n','')+'\n')
