import json
import numpy as np
#a = np.array([ 0.7972,  0.0767,  0.4383,  0.7866,  0.8091,  0.1954,
 #                  0.6307, 0.6599,  0.1065,  0.0508])
from scipy import stats
#>>> stats.zscore(a)
checklist=list()
featuredict=list()
lastfeature=None
with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data.txt', mode='r') as writer:
        for line in writer:
            checklist.append(json.loads(line))

for  data in checklist:
        timefeaturelist=dict()
        for i in range(49):
            featurelist=list()
            featurelist.append(data['maplenthofTweet'][i])
            featurelist.append(data['mapPositiveScoer'][i])
            featurelist.append(data['mapNumPositive'][i])
            featurelist.append(data['mapPositiveWord'][i])
            featurelist.append(data['mapURL'][i])
            featurelist.append(data['mapHashtag'][i])
            featurelist.append(data['mapI'][i])
            featurelist.append(data['mapMention'][i])
            featurelist.append(data['mapQuestion'][i])
            featurelist.append(data['mapExclamation'][i])
            featurelist.append(data['mapQuestionExclamation'][i])
            featurelist.append(data['mapUserDescription'][i])
            featurelist.append(data['mapUserPhoto'][i])
            featurelist.append(data['mapUsersInLargeCity'][i])
            featurelist.append(data['mapUserFollower'][i])
            featurelist.append(data['mapUserFollowing'][i])
            featurelist.append(data['mapUserPost'][i])
            featurelist.append(data['mapUserResistation'][i])
            featurelist.append(data['mapUserReputationScore'][i])
            timefeaturelist['F'+str(i)]=(featurelist)
            if lastfeature is not None:
                Slist=np.array(featurelist)-np.array(lastfeature)
                timefeaturelist['S'+str(i-1)]=(Slist.tolist())
            lastfeature=featurelist
        lastfeature=None
        mydict=dict()
        mydict['title']=data['name']
        mydict['data']=timefeaturelist
        if len(timefeaturelist)!=97:
            print(mydict['title'])
        featuredict.append(mydict)

def normail(num):
    maxim=max(num)
    if maxim == 0:
        return num
    minim =min(num)
    temp=[]
    for nu in num:
        temp.append(float(nu-minim)/(maxim-minim))
    return temp
for fs in featuredict:
    for fea in fs['data'].keys():
        if max(fs['data'][fea])!=min(fs['data'][fea]):
            fs['data'][fea]=(stats.zscore(np.array(fs['data'][fea])).tolist())
        #fs['data'][fea]=normail(fs['data'][fea])
    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data-nomal.txt', mode='a') as writer:
        #print(fs)
        JSON=json.dumps(fs)
        writer.write(JSON + '\n')
            # data['maplenthofTweet']=stats.zscore(np.array(data['maplenthofTweet'])).tolist()
            # data['mapPositiveScoer']=stats.zscore(np.array(data['mapPositiveScoer'])).tolist()
            # data['mapNumPositive']=stats.zscore(np.array(data['mapNumPositive'])).tolist()
            # data['mapPositiveWord']=stats.zscore(np.array(data['mapPositiveWord'])).tolist()
            # data['mapURL']=stats.zscore(np.array(data['mapURL'])).tolist()
            # data['mapHashtag']=stats.zscore(np.array(data['mapHashtag'])).tolist()
            # data['mapI']=stats.zscore(np.array(data['mapI'])).tolist()
            # data['mapMention']= stats.zscore(np.array(data['mapMention'])).tolist()
            # data['mapQuestion']=stats.zscore(np.array(data['mapQuestion'])).tolist()
            # data['mapExclamation']=stats.zscore(np.array(data['mapExclamation'])).tolist()
            # data['mapQuestionExclamation']=stats.zscore(np.array(data['mapQuestionExclamation'])).tolist()
            # data['mapUserDescription']=stats.zscore(np.array(data['mapUserDescription'])).tolist()
            # data['mapUserPhoto']=stats.zscore(np.array(data['mapUserPhoto'])).tolist()
            # data['mapUsersInLargeCity']=stats.zscore(np.array(data['mapUsersInLargeCity'])).tolist()
            # data['mapUserFollower']=stats.zscore(np.array(data['mapUserFollower'])).tolist()
            # data['mapUserFollowing']=stats.zscore(np.array(data['mapUserFollowing'])).tolist()
            # data['mapUserPost']=stats.zscore(np.array(data['mapUserPost'])).tolist()
            # data['mapUserResistation']=stats.zscore(np.array(data['mapUserResistation'])).tolist()
            # data['mapUserReputationScore']=stats.zscore(np.array(data['mapUserReputationScore'])).tolist()
            #nomalizelist.append(data)
        # with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data-nomal2.txt', mode='a') as writer:
        #     JSON=json.dumps(data)
        #     writer.write(JSON + '\n')
