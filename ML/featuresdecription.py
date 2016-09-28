import path
import json
Userfeaturefull=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserJoin_date','UserDescription','Usertweets_count',
                   'Userverified','UserNumphoto','UserIsInLargeCity']



Userfeaturesingle=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserJoin_date','UserDescription','Usertweets_count',
                   'Userverified']


Textfeaturesingle=['lenthofTweet','NumChar','Capital',
                   'Smile','Sad','NumPositiveWords','NumNegativeWords','PositiveScoer',
                   'I','You','HeShe',
                   'Via','Stock','Question','Exclamation','QuestionExclamation']


Textfeaturesingle_old=['lenthofTweet','NumPositiveWords','PositiveScoer',
                   'I',
                   'Question','Exclamation','QuestionExclamation']

Tweetfeaturesingle=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites',
                    'Contain_videos']
Tweetfeaturesfull=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites','ContainNEWS',
                    'Contain_videos','WotScore','UrlRankIn5000','UrlRank']

Tweetfeaturesingle_Old=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites']

SpikeM=['Ps','Pa','Pp','Qp','Qa','Qs']
#SpikeM=[ 'Pa' ]
SIR=['beta','gamma']
creditScor=['creditScore']
crowdwisdom=['DebunkingWords']

AllfeaturesingleOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old
Allfeaturesingle=Userfeaturesingle+Textfeaturesingle+Tweetfeaturesingle


Allfeaturefull=Textfeaturesingle+Userfeaturefull+Tweetfeaturesfull+SpikeM+creditScor+crowdwisdom+SIR
AllfeaturefullOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old#+['creditScore']
Allfeaturefullwithoutcredit=Textfeaturesingle+Userfeaturefull+SpikeM+Tweetfeaturesingle



pickfeature= ['UserNumphoto','QuestionExclamation','UserrepitationScore','Userfollowers_count','UserrepitationScore',
              'Question','Userfriends_count','DebunkingWords','ContainNEWS','creditScore','Usertweets_count',
              'Pa','Via','WotScore','You','numUrls','NumPhotos','UserNumphoto','Menstion','UserIsInLargeCity',
              'I','Capital','Userverified','UserDescription','UrlRankIn5000','NumChar','gamma','PositiveScoer']  #['WotScore']#+Userfeaturesingle+Textfeaturesingle_old+['Hashtag','Menstion','numUrls','Retweets','Isretweet','NumPhotos','Favorites']
featureTypes={'Userfeature':Userfeaturefull,'Textfeature':Textfeaturesingle,'Tweetfeature':Tweetfeaturesfull,'creditScore':creditScor,
              "spikM":SpikeM,'crowdwisdom':crowdwisdom,'allfeature':Allfeaturefull,'SIR':SIR,'bestset':pickfeature
              }


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