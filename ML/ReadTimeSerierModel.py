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
    model = RandomForestClassifier(n_estimators=200,random_state=0,n_jobs=4)
    model.fit(train_x, train_y)
    return model


def MLP_classifier(train_x, train_y):
    clf = MLPClassifier(activation='relu', algorithm='adam', alpha=0.001,
               batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=False,
               epsilon=1e-08, hidden_layer_sizes=([10,10]), learning_rate='constant',
               learning_rate_init=0.01, max_iter=300, momentum=0.9,
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
    for i in range(maxtime+1):
        index.append('F'+str(i))
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
#print(indeslixt[:5])

#pickedFeatures=featuresdecription.pickfeature
pickedFeatures=['ContainNEWS']

times=10
lenofpiece=int(len(indeslixt)/times+0.5)
rumorout=[]
newsout=[]
for maxtime in range(0,49):
    scores=[]
    listofPara=list()
    listofresult=list()

    listofParatest=list()
    listofresulttest=list()
    rumortw=0
    newtw=0
    for rumor in listofrumor:
        # if rumor['eventID']==307:
        listofPara=getFeauture(rumor,maxtime,pickedFeatures)
        for eee in listofPara:
            # print(eee)
            rumortw+=eee

    # rumor = listofnews[5]
    for news in listofnews:
        # if news['eventID']==207:
        listofPara=getFeauture(news,maxtime,pickedFeatures)
        for eee in listofPara:
            newtw+=eee
            # print(eee)
    # print(maxtime)
    rumorout.append(rumortw/len(listofrumor)/(maxtime+1))
    newsout.append(newtw/len(listofnews)/(maxtime+1))
for ee in rumorout:
    print(ee)


print('end')
for ee in newsout:
    print(ee)
