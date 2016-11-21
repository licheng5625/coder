from sklearn import svm
import numpy
import json
import random
from sklearn import datasets, metrics,cross_validation
import csv

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

def Extra_Trees_classifier(train_x, train_y):
    from sklearn.ensemble import ExtraTreesClassifier
    model = ExtraTreesClassifier(n_estimators=1000,random_state=1)
    model.fit(train_x, train_y)
    return model


def MLP_classifier(train_x, train_y):
    clf = MLPClassifier(activation='relu', algorithm='adam', alpha=0.001,
               batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=False,
               epsilon=1e-08, hidden_layer_sizes=([5,5]), learning_rate='constant',
               learning_rate_init=0.01, max_iter=500, momentum=0.9,
               nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
               tol=0.0001, validation_fraction=0.1, verbose=False,
               warm_start=False)
    clf.fit(train_x, train_y)
    return clf

def SVM_classifier(train_x, train_y):
    clf = svm.SVC(C=1)
    clf.fit(train_x, train_y)
    return clf
featuresIndes=[]

def getFeauture(tweet,maxtime,indexfeatureslist):
    global featuresIndes
    features=tweet['features']
    allfeaturelist=[]
    index=[]
    index.append('F'+str(maxtime))

    # for i in range(maxtime+1):
    #     index.append('F'+str(i))
    #     if i !=0:
    #         index.append('S'+str(i))
    for key in index:
        featureslist=[]
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
#
# dddd=[[0,1],[2,3],[4,5]]
# print(dddd[:,1])

indeslixt=[]
with open(path.Featurepath+'indexshuffled.txt',encoding='utf-8',mode='r') as writer:
     indeslixt=json.loads(writer.read())

pickedFeatures=featuresdecription.Allfeaturefull
times=10
lenofpiece=int(len(indeslixt)/times+0.5)
with open(path.Featurepath+"rankedfeatures_importance_1302.csv",encoding='utf-8', mode='w') as csvfile:
    writermix = csv.DictWriter(csvfile, fieldnames=['time']+pickedFeatures)
    writermix.writeheader()
    resultovertime={}
    for maxtime in range(1,49):
        if maxtime not in [1,6,12,24,48]:
            continue
        result={}
         # 1---48 hors
        scores=[]
        importancesall=[]

        for time in range(times):

            listofPara=list()
            listofresult=list()

            listofParatest=list()
            listofresulttest=list()
            for rumor in listofrumor:
                if rumor['eventID'] not in  indeslixt[time*lenofpiece: time*lenofpiece+lenofpiece]:
                    listofPara.append(getFeauture(rumor,maxtime,pickedFeatures))
                    listofresult.append(1)
                else:
                    listofParatest.append(getFeauture(rumor,maxtime,pickedFeatures))
                    listofresulttest.append(1)

            for news in listofnews:
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

        # clf = SVM_classifier(listofPara, listofresult)
        #clf=MLP_classifier(listofPara, listofresult)

            clf=random_forest_classifier(listofPara, listofresult)
            importances=clf.feature_importances_
            for im in range(len(importances)):
                try:
                    importancesall[im]+=importances[im]
                except IndexError:
                    importancesall =importances
                    break
        results={}
        for i in range(len(pickedFeatures)):
            results[pickedFeatures[i]]=importances[i]/times
        sortkeys=sorted(results, key=results.__getitem__,reverse=True)
        i=0
        rankedresult={}
        for key in sortkeys:
            rankedresult [key]=i
            try:
                resultovertime[key]+=i
            except :
                resultovertime[key]=i
            i+=1
        #rankedfeature=results
        results['time']=maxtime
        writermix.writerow(rankedresult)
        output=''
        counter=0
        for key in sortkeys:
            counter+=1
            output+='\''+key+'\''+','
        print(output)
         #writermix.writerow(results)

sortkeys=sorted(resultovertime, key=resultovertime.__getitem__,reverse=False)
maxnum=26
counter=0
output=''
for key in sortkeys:
    counter+=1
    output+='\''+key+'\''+','
    # if counter==26:
    #     break
print(output)
output=''

for key in sortkeys:
    counter+=1
    output+='\''+key+'\''+','
print(output)