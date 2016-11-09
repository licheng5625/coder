from sklearn import svm
import numpy
import json
import random
from sklearn import datasets, metrics,cross_validation
listofrumor=list()
listofnews=list()
import  mypath as path
import featuresdecription
from sklearn.neural_network import MLPClassifier

from scipy import stats
from sklearn.preprocessing import StandardScaler

with open(path.Featurepath+'featuresRumorsTimeSerior130.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

with open(path.Featurepath+'featuresNewsTimeSerior130.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofnews.append(JSON)


def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=350,random_state=0,n_jobs=4)
    model.fit(train_x, train_y)
    return model


def MLP_classifier(train_x, train_y):
    clf = MLPClassifier(activation='relu', algorithm='adam', alpha=0.0001,
               batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=True,
               epsilon=1e-08, hidden_layer_sizes=([50,50]), learning_rate='constant',
               learning_rate_init=0.01, max_iter=3000, momentum=0.9,
               nesterovs_momentum=True, power_t=0.5, random_state=0, shuffle=True,
                validation_fraction=0.1, verbose=False,
               warm_start=False)
    clf.fit(train_x, train_y)
    return clf

def SVM_classifier(train_x, train_y):
    clf = svm.SVC(C=3,random_state=0)
    clf.fit(train_x, train_y)
    return clf
featuresIndes=[]

def getFeauture(tweet,maxtime,indexfeatureslist):
    global featuresIndes
    features=tweet['features']
    allfeaturelist=[]
    index=[]

    # index.append('F'+str(maxtime))
    # for i in range(maxtime+1):
    index.append('F'+str(maxtime))
        # if i !=0:
        #     index.append('S'+str(i))
    for key in index:
        featureslist=[]
        #for featureIndex in featuresdecription.AllfeaturefullOld:#
        for featureIndex in indexfeatureslist:
            featureslist.append(features[key][featureIndex])
            featuresIndes.append(featureIndex)
            #print(featureIndex)
        #featureslist=stats.zscore(numpy.array(featureslist)).tolist()
        allfeaturelist=allfeaturelist+featureslist
        # def isNaN(num):
        #     return num != num
        # for i in range(len(allfeaturelist)):#72278338945
        #     if isNaN(allfeaturelist[i]):
        #         allfeaturelist[i]=0
        #allfeaturelist=stats.zscore(numpy.array(allfeaturelist)).tolist()
    return allfeaturelist

indeslixt=[]
# for i in range(len(listofrumor)+len(listofnews)):
#     indeslixt.append(i)
#     i+=1
# for rumor in listofrumor:
#     indeslixt.append(rumor['eventID'])
# for news in listofnews:
#     indeslixt.append(news['eventID'])
# random.seed(0)
# random.shuffle(indeslixt)
with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
    indeslixt=json.loads(writer.read())
    dsdsds=[]
    for news in listofnews:
        dsdsds.append(news['eventID'])
    for news in listofrumor:
        dsdsds.append(news['eventID'])

    for index in indeslixt:
        if index not in dsdsds:
            print(index)
#print(indeslixt[:5])

#pickedFeatures=featuresdecription.pickfeature
pickedFeatures=featuresdecription.Allfeaturefullstatic

times=10
lenofpiece=int(len(indeslixt)/times+0.5)

for maxtime in range(1,49):
    scores=[]
    # if maxtime%6!=0 and maxtime!=1:
    #     continue
    for time in range(times):
        listofPara=list()
        listofresult=list()

        listofParatest=list()
        listofresulttest=list()

        for rumor in listofrumor:
            if rumor['eventID'] not in indeslixt:
                continue
            if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                listofPara.append(getFeauture(rumor,maxtime,pickedFeatures))
                listofresult.append(1)
            else:
                listofParatest.append(getFeauture(rumor,maxtime,pickedFeatures))
                listofresulttest.append(1)

        for news in listofnews:
            if news['eventID'] not in indeslixt:
                continue

            if news['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                listofPara.append(getFeauture(news,maxtime,pickedFeatures))
                listofresult.append(-1)
            else:
                listofParatest.append(getFeauture(news,maxtime,pickedFeatures))
                listofresulttest.append(-1)
        # scaler = StandardScaler()
        # scaler.fit(listofPara)
        # listofPara = scaler.transform(listofPara)
        # listofParatest = scaler.transform(listofParatest)

        #clf = SVM_classifier(listofPara, listofresult)
        # clf=MLP_classifier(listofPara, listofresult)

        clf=random_forest_classifier(listofPara, listofresult)
        score = metrics.recall_score(clf.predict(listofParatest), (listofresulttest))

        # score = metrics.accuracy_score(clf.predict(listofParatest), (listofresulttest))
        scores.append(score)
    avg=sum(scores) / float(len(scores))
    print(str(avg))



    # def getscore(times,listofPara,listofresult):
    #     scores=[]
    #     scaler = StandardScaler()
    #     scaler.fit(listofPara)
    #     listofPara = scaler.transform(listofPara)
    #     #templistoftestpara = scaler.transform(templistoftestpara)
    #
    #     for time in range(times):
    #         templistofpara=[]
    #         templistofresult=[]
    #         templistoftestpara=[]
    #         templistoftestresult=[]
    #         #print((indeslixt))
    #         for event in listofPara:
    #             if event['eventID'] not in  indeslixt[time*int(len(listofPara)/times):time*int(len(listofPara)/times)+int(len(listofPara)/times)]:
    #                 templistofpara.append(listofPara[eee])
    #                 templistofresult.append(listofresult[eee])
    #             else:
    #                 templistoftestpara.append(listofPara[eee])
    #                 templistoftestresult.append(listofresult[eee])
    #         #clf = SVM_classifier(templistofpara, templistofresult)
    #         #clf=MLP_classifier(templistofpara, templistofresult)
    #         clf=random_forest_classifier(templistofpara, templistofresult)
    #         #clf.fit(templistofpara, templistofresult)
    #         print(clf.predict(templistoftestpara))
    #         score = metrics.accuracy_score(clf.predict(templistoftestpara), (templistoftestresult))
    #         scores.append(score)
    #
    #     return scores



    #scores=getscore(10,listofPara,listofresult)
    #avg=sum(scores) / float(len(scores))
    #print(str(avg))
    #print('  '+str(maxtime)+'    '+str(avg))

#
# 0.77619047619
# 0.793650793651
# 0.768253968254
# 0.757142857143
# 0.768253968254
# 0.771428571429
# 0.779365079365
# 0.785714285714
# 0.790476190476
# 0.834920634921
# 0.815873015873
# 0.849206349206
# 0.87619047619
# 0.863492063492
# 0.874603174603
# 0.849206349206
# 0.852380952381
# 0.919047619048
# 0.852380952381
# 0.919047619048
# 0.860317460317
# 0.919047619048
# 0.930158730159
# 0.885714285714
