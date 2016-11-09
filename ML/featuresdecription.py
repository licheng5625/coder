import path
import json
Userfeaturefull=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserJoin_date','UserDescription','UserTweetsPerDays',#'Usertweets_count',
                   'Userverified','UserNumphoto','UserIsInLargeCity']



Userfeaturesingle=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserDescription','Usertweets_count',
                   'Userverified']


Textfeaturesingle=['lenthofTweet','NumChar','Capital',
                   'Smile','Sad','NumPositiveWords','NumNegativeWords','PositiveScoer',
                   'I','You','HeShe',
                   'Via','Stock','Question','Exclamation','QuestionExclamation']


Textfeaturesingle_old=['lenthofTweet','NumPositiveWords','PositiveScoer',
                   'I',
                   'Question','Exclamation','QuestionExclamation']

Tweetfeaturesingle=['Hashtag','Menstion','numUrls','Retweets','Isretweet']
Tweetfeaturesfull=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                   'ContainNEWS',
                    'WotScore','UrlRankIn5000']#,'UrlRank']

Tweetfeaturesingle_Old=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites']

SpikeM=['Ps','Pa','Pp','Qp','Qa','Qs']
#SpikeM=[ 'Pa' ]
SIR=['beta','gamma','B','b','l','e','p','rho','SEIZIndex']
creditScor=['creditScore']
crowdwisdom=['DebunkingWords']

AllfeaturesingleOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old
Allfeaturesingle=Userfeaturesingle+Textfeaturesingle+Tweetfeaturesingle


Allfeaturefull=Textfeaturesingle+Userfeaturefull+Tweetfeaturesfull+SpikeM+creditScor+crowdwisdom+SIR
AllfeaturefullOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old#+['creditScore']
Allfeaturefullwithoutcredit=Textfeaturesingle+Userfeaturefull+SpikeM+Tweetfeaturesingle+crowdwisdom+SIR
Allfeaturefullstatic=Textfeaturesingle+Userfeaturefull+Tweetfeaturesingle+crowdwisdom+creditScor

pickfeature= ['creditScore','ContainNEWS','DebunkingWords','QuestionExclamation',
              'NumChar','UserrepitationScore','Question','UrlRankIn5000','UserJoin_date',
              'WotScore','Exclamation','UserTweetsPerDays','Menstion','Userfollowers_count',
              'Userverified','You','lenthofTweet','Via','UserIsInLargeCity','Hashtag','UserDescription',
              'numUrls','Pa','NumPositiveWords','B','b']#,'SEIZIndex',
               #'PositiveScoer','e']

pickfeature2= ['creditScore','DebunkingWords','ContainNEWS','UserTweetsPerDays',
               'UserrepitationScore','UrlRankIn5000','NumChar','QuestionExclamation',
               'WotScore','UserJoin_date','Exclamation','Question','Menstion','Userfollowers_count',
               'lenthofTweet','Userverified','numUrls','Hashtag','Via','UserDescription','You',
               'NumPositiveWords','UserIsInLargeCity','Pa','UserNumphoto']
               #'PositiveScoer','e']
#['WotScore']#+Userfeaturesingle+Textfeaturesingle_old+['Hashtag','Menstion','numUrls','Retweets','Isretweet','NumPhotos','Favorites']

featureTypes={'bestset':pickfeature
                # ,'bestset2':pickfeature2
             ,'Userfeature':Userfeaturefull,'Textfeature':Textfeaturesingle,'Tweetfeature':Tweetfeaturesfull,'creditScore':creditScor
          , "spikM":SpikeM,'crowdwisdom':crowdwisdom,'allfeature':Allfeaturefull,'SIR':SIR,'no creditScore':Allfeaturefullwithoutcredit}

def getNewsEventID():
    id=[]
    with open (path.Featurepath+'descriptionNews.txt',encoding='utf-8',mode='r') as text:
        for line in text:
            id.append(json.loads(line)['eventID'])
    return id

def getRumorEventID():
    id=[]
    with open (path.Featurepath+'featuresRumors.txt',encoding='utf-8',mode='r') as text:
        for line in text:
            id.append(json.loads(line)['eventID'])
    return id

def getAllEventID():

    return getRumorEventID()+getNewsEventID()