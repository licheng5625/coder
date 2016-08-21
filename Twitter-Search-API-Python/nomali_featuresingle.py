import json
import numpy as np
#a = np.array([ 0.7972,  0.0767,  0.4383,  0.7866,  0.8091,  0.1954,
 #                  0.6307, 0.6599,  0.1065,  0.0508])
from scipy import stats
import csv
import path
from  random  import random

#>>> stats.zscore(a)
rumorlist=list()
newslist=list()

lastfeature=None
with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/datasingle.txt', mode='r') as writer:
        for line in writer:
            rumorlist.append(json.loads(line))
with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/datasingleNews.txt', mode='r') as writer:
        for line in writer:
            newslist.append(json.loads(line))
# p="123456"
# print(p[:-1])
# print(p[-1])


def normail(num):
    maxim=max(num)
    if maxim == 0:
        return num
    minim =min(num)
    temp=[]
    for nu in num:
        temp.append(float(nu-minim)/(maxim-minim))
    return temp
with open(path.TweetJSONpath+'newssingletest.txt', 'w') as newstxt:
    with open(path.TweetJSONpath+'rumorsingletest.txt', 'w') as rumorstxt:

        with open(path.TweetJSONpath+'test.csv', 'w') as testcsvfile:
            fieldnames = ['maplenthofTweet', 'mapPositiveScoer','mapNumPositiveWords','Urls','Hashtag','I','Menstion',
                          'Question','Exclamation','UserDescription',
                          'verified','followers_count','friends_count','tweets_count','RepitationScore','Days','rumor','new']
                          # ,'smile','Sad','HeShe','U','via','contain_videos','stock','numchar','capital'
                          # ,'isretweet','retweets','favorites','WOT','mapNumNegativeWords','rumor','new']
            testwriter=csv.DictWriter(testcsvfile, fieldnames=fieldnames)
            #testwriter.writeheader()

            with open(path.TweetJSONpath+'train.csv', 'w') as csvfile:

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    #writer.writeheader()
                    countertrain=0.0
                    countertext=0.0

                    for fea in rumorlist:
                        #for fea in fs:
                            if max(fea[:-1])!=min(fea[:-1]):
                                result=fea[-1]
                                fea=(stats.zscore(np.array(fea[:-1])).tolist())
                                fea.append(result)
                                rumor=0
                                news=0
                                if fea[-1] ==-1:
                                    rumor=1
                                else:
                                    news=1
                                faeturewriter=None
                                featurelist=[]
                                featurelist=fea[:-1]
                                # featurelist.append(fea[0])
                                # featurelist.append(fea[1])
                                # featurelist.append(fea[2])
                                # featurelist.append(fea[4])
                                # featurelist.append(fea[7])
                                # featurelist.append(fea[16])
                                # featurelist.append(fea[21])
                                # featurelist.append(fea[22])
                                # featurelist.append(fea[23])
                                # featurelist.append(fea[24])
                                # featurelist.append(fea[25])
                                # featurelist.append(fea[26])
                                # featurelist.append(fea[27])
                                # featurelist.append(fea[28])
                                # featurelist.append(fea[29])
                                # featurelist.append(fea[30])
                                featurelist.append(1)

                                rumorstxt.write(json.dumps(featurelist)+'\n')
                                if random()>0.1:
                                    countertrain+=1
                                    faeturewriter=writer
                                    # writer.writerow({'maplenthofTweet': fea[0], 'mapPositiveScoer': fea[1],
                                    #                  'mapNumPositiveWords': fea[2],'mapNumNegativeWords': fea[3], 'Urls': fea[4],
                                    #                  'WOT': fea[5],'favorites':fea[6],
                                    #                  'Hashtag': fea[7],'isretweet':fea[8],'retweets':fea[9],
                                    #                  'contain_videos':fea[11],'stock': fea[12],'numchar': fea[13],
                                    #                  'capital': fea[14],'via': fea[15],'I': fea[16],
                                    #                  'smile': fea[17],'Sad': fea[18],'HeShe': fea[19],'U': fea[20],
                                    #                  'Menstion': fea[21], 'Question': fea[22],
                                    #                  'Exclamation': fea[23], 'UserDescription': fea[24],
                                    #                  'verified': fea[25], 'followers_count': fea[26],
                                    #                  'friends_count': fea[27], 'tweets_count': fea[28],
                                    #                  'RepitationScore': fea[29], 'Days': fea[30],'rumor':rumor,'new':news
                                    #                  })
                                else:
                                    countertext+=1
                                    faeturewriter=testwriter

                                faeturewriter.writerow({'maplenthofTweet': fea[0], 'mapPositiveScoer': fea[1],
                                                 'mapNumPositiveWords': fea[2], 'Urls': fea[4],

                                                 'Hashtag': fea[7],'I': fea[16],

                                                 'Menstion': fea[21], 'Question': fea[22],
                                                 'Exclamation': fea[23], 'UserDescription': fea[24],
                                                 'verified': fea[25], 'followers_count': fea[26],
                                                 'friends_count': fea[27], 'tweets_count': fea[28],
                                                 'RepitationScore': fea[29], 'Days': fea[30],'rumor':rumor,'new':news
                                                 })
                    for fea in newslist:
                        if max(fea[:-1])!=min(fea[:-1]):
                                result=fea[-1]
                                fea=(stats.zscore(np.array(fea[:-1])).tolist())
                                fea.append(result)
                                rumor=0
                                news=0
                                if fea[-1] ==-1:
                                    rumor=1
                                else:
                                    news=1

                                faeturewriter=None
                                featurelist=[]
                                featurelist=fea[:-1]
                                # featurelist.append(fea[0])
                                # featurelist.append(fea[1])
                                # featurelist.append(fea[2])
                                # featurelist.append(fea[4])
                                # featurelist.append(fea[7])
                                # featurelist.append(fea[16])
                                # featurelist.append(fea[21])
                                # featurelist.append(fea[22])
                                # featurelist.append(fea[23])
                                # featurelist.append(fea[24])
                                # featurelist.append(fea[25])
                                # featurelist.append(fea[26])
                                # featurelist.append(fea[27])
                                # featurelist.append(fea[28])
                                # featurelist.append(fea[29])
                                # featurelist.append(fea[30])
                                featurelist.append(-1)
                                newstxt.write(json.dumps(featurelist)+'\n')

                                if random()>0.1:
                                    countertrain+=1
                                    faeturewriter=writer
                                    # writer.writerow({'maplenthofTweet': fea[0], 'mapPositiveScoer': fea[1],
                                    #                  'mapNumPositiveWords': fea[2],'mapNumNegativeWords': fea[3], 'Urls': fea[4],
                                    #                  'WOT': fea[5],'favorites':fea[6],
                                    #                  'Hashtag': fea[7],'isretweet':fea[8],'retweets':fea[9],
                                    #                  'contain_videos':fea[11],'stock': fea[12],'numchar': fea[13],
                                    #                  'capital': fea[14],'via': fea[15],'I': fea[16],
                                    #                  'smile': fea[17],'Sad': fea[18],'HeShe': fea[19],'U': fea[20],
                                    #                  'Menstion': fea[21], 'Question': fea[22],
                                    #                  'Exclamation': fea[23], 'UserDescription': fea[24],
                                    #                  'verified': fea[25], 'followers_count': fea[26],
                                    #                  'friends_count': fea[27], 'tweets_count': fea[28],
                                    #                  'RepitationScore': fea[29], 'Days': fea[30],'rumor':rumor,'new':news
                                    #                  })
                                else:
                                    countertext+=1
                                    faeturewriter=testwriter

                                faeturewriter.writerow({'maplenthofTweet': fea[0], 'mapPositiveScoer': fea[1],
                                                 'mapNumPositiveWords': fea[2], 'Urls': fea[4],

                                                 'Hashtag': fea[7],'I': fea[16],

                                                 'Menstion': fea[21], 'Question': fea[22],
                                                 'Exclamation': fea[23], 'UserDescription': fea[24],
                                                 'verified': fea[25], 'followers_count': fea[26],
                                                 'friends_count': fea[27], 'tweets_count': fea[28],
                                                 'RepitationScore': fea[29], 'Days': fea[30],'rumor':rumor,'new':news
                                                 })

                    print(countertrain)
                    print(countertext)

            #fs['data'][fea]=normail(fs['data'][fea])
            # with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data-nomal-single.txt', mode='a') as writer:
            #     #print(fs)
            #     JSON=json.dumps(fea)
            #     writer.write(JSON + '\n')
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
