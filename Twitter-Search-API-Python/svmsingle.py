from sklearn import svm
import numpy
import json
import random
from sklearn import datasets, metrics
listofrumor=list()
listofnews=list()

with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/rumorsingletest.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofrumor.append(JSON)

with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/newssingletest.txt', mode='r') as writer:
    for line in writer:
        JSON=json.loads(line)
        listofnews.append(JSON)

print(len(listofnews))

for indexoffeaturelow in range(16,17):

    listofPara=list()
    listofresult=list()

    listofParatest=list()
    listofresulttest=list()

    for i in range (0,20000):#len(listofnews)-5):
        temp=[]
        temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        listofPara.append(temp)
        listofresult.append(1)

    for i in range (0,20000):#len(listofnews)-5):
        temp2=[]
        temp2=temp2+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        listofPara.append(temp2)
        listofresult.append(-1)

    for i in range (len(listofnews)-1000,len(listofnews)):
        temp=[]
        temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        listofParatest.append(temp)
        listofresulttest.append(1)
    for i in range (len(listofnews)-1000,len(listofnews)):
        temp=[]
        temp=temp+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
        listofParatest.append(temp)
        listofresulttest.append(-1)


    # import tensorflow as tf
    #
    # clf = tf.contrib.learn.DNNClassifier(hidden_units=[10, 20, 10], n_classes=2)
    # import numpy as np
    # # Fit model
    # clf.fit(x=np.array(listofParatest), y=np.array(listofresult), steps=500)
    # #
    # print(clf.predict(np.array(listofParatest)))
    # score = metrics.accuracy_score(clf.predict(np.array(listofParatest)),np.array(listofresulttest))
    # print(score)
    from sklearn import cross_validation
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
        for time in range(times):
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
            for eee in range(len(listofPara)):
                if eee in indeslixt[10:]:
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
    #
    #print( clf.predict(listofParatest))
    #print(clf.predict((listofParatest)))
    #score = metrics.accuracy_score(clf.predict((listofParatest)), (listofresulttest))
    #print(score)
    clf = svm.SVC(kernel='linear',C=2,random_state=0)
    clf.fit(listofPara, listofresult)
    score = metrics.accuracy_score(clf.predict((listofParatest)), (listofresulttest))
    print(score)
    #print(listofresulttest)

    #scores = cross_validation.cross_val_score( clf, listofPara, listofresult, cv=10)
    #for i in range(50):
    #scores=getscore(40,listofPara,listofresult)
    #scores=getscore2(listofPara,listofresult)

    #avg=sum(scores) / float(len(scores))
    #print(str(avg))
