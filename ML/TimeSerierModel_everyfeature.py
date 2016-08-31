from sklearn import svm
import numpy
import json
import random
from sklearn import datasets, metrics,cross_validation
listofrumor=list()
listofnews=list()
import  path
import featuresdecription
from sklearn.neural_network import MLPClassifier

from scipy import stats
from sklearn.preprocessing import StandardScaler

with open(path.Featurepath+'featuresRumorsTimeSerior.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

with open(path.Featurepath+'featuresNewsTimeSerior.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofnews.append(JSON)


def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
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
    for i in range(maxtime+1):
        index.append('F'+str(i))
        if i !=0:
            index.append('S'+str(i))
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




for feature in featuresdecription.Allfeaturefull:
    result=[]
    # 1---48 hors
    for maxtime in range(1,49):
        listofPara=list()
        listofresult=list()

        listofParatest=list()
        listofresulttest=list()

        for rumor in listofrumor:
            listofPara.append(getFeauture(rumor,maxtime,[feature]))
            listofresult.append(1)
        for news in listofnews:
            listofPara.append(getFeauture(news,maxtime,[feature]))
            listofresult.append(-1)


        def getscore2(listofPara,listofresult):
            scores=[]
            indeslixt=[]
            for i in range(len(listofPara)):
                    indeslixt.append(i)
                    i+=1
            random.seed()
            random.shuffle(indeslixt)
            templistofpara=[]
            templistofresult=[]
            templistoftestpara=[]
            templistoftestresult=[]
            #print(indeslixt[:5])
            for eeee in range(len(listofPara)):
                for eee in range(len(listofPara)):
                    if eee != indeslixt[eeee]:
                        templistofpara.append(listofPara[eee])
                        templistofresult.append(listofresult[eee])
                    else:
                        templistoftestpara.append(listofPara[eee])
                        templistoftestresult.append(listofresult[eee])
                clf = svm.SVC()
                clf.fit(templistofpara, templistofresult)
                score = metrics.accuracy_score(clf.predict((templistoftestpara)), (templistoftestresult))
                scores.append(score)
                clf=None
            return scores

        def getscore(times,listofPara,listofresult):
            scores=[]
            scaler = StandardScaler()
            scaler.fit(listofPara)
            listofPara = scaler.transform(listofPara)
            #templistoftestpara = scaler.transform(templistoftestpara)

            for time in range(times):
                indeslixt=[]
                for i in range(len(listofPara)):
                    indeslixt.append(i)
                    i+=1
                random.seed(time)

                random.shuffle(indeslixt)
                templistofpara=[]
                templistofresult=[]
                templistoftestpara=[]
                templistoftestresult=[]
                #print((indeslixt))
                for eee in range(len(listofPara)):
                    if eee in indeslixt[0:80]:
                        templistofpara.append(listofPara[eee])
                        templistofresult.append(listofresult[eee])
                    else:
                        templistoftestpara.append(listofPara[eee])
                        templistoftestresult.append(listofresult[eee])
                #clf = SVM_classifier(templistofpara, templistofresult)
                #clf=MLP_classifier(templistofpara, templistofresult)
                clf=random_forest_classifier(templistofpara, templistofresult)
                #clf.fit(templistofpara, templistofresult)
                score = metrics.accuracy_score(clf.predict(templistoftestpara), (templistoftestresult))
                scores.append(score)
            # importances = clf.feature_importances_
            # std = numpy.std([tree.feature_importances_ for tree in clf.estimators_],
            #              axis=0)
            # indices = numpy.argsort(importances)[::-1]
            # print("Feature ranking:")
            # global featuresIndes
            # for f in range(len(templistofpara[1])):
            #     print("%d. feature %s (%f)" % (f + 1, featuresIndes[f], importances[indices[f]]))

            return scores
        #
        #print( clf.predict(listofParatest))
        #print(clf.predict((listofParatest)))
        #clf = svm.SVC(C=1)
        #clf=random_forest_classifier
        # scaler = StandardScaler()
        # scaler.fit(listofPara)
        # listofPara = scaler.transform(listofPara)
        # scores = cross_validation.cross_val_score( clf, listofPara, listofresult, cv=9)
        # print(sum(scores) / float(len(scores)))



        scores=getscore(20,listofPara,listofresult)
        avg=sum(scores) / float(len(scores))
        result.append(avg)
    avg=sum(result) / float(len(result))
    print(feature +'    '+str(avg))
    #print('  '+str(maxtime)+'    '+str(avg))

  # 1    0.721875
  # 2    0.778125
  # 3    0.81875
  # 4    0.753125
  # 5    0.809375
  # 6    0.803125