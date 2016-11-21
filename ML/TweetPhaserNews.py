import findspark
import os
from nltk.sentiment.util import getPositiveWords
from nltk.sentiment.util import getNegativeWords
import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.parse import urlparse
import mypath as path

sid = SentimentIntensityAnalyzer()
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import json
findspark.init(spark_home=path.sparkpath)

from pyspark import SparkContext, SparkConf

import datetime


conf = SparkConf().setAppName("Spark Count")
sc = SparkContext(conf=conf)


datafolder=path.TweetRAWpath+'newNews/'
outputFile=path.TweetJSONpath+'newsddd/'
# datafolder=path.TweetJSONpath+'rumors/'
# descriptionFile=path.TweetJSONpath+'descriptionRumors.txt'
# outputFile=path.Featurepath+'featuresrumorsnewset.txt'

timeformate='%I:%M %p - %d %b %Y'
timetoday=datetime.datetime.strptime("10 7 2016",'%d %m %Y')
list_dirs = os.walk(datafolder)
selectindex=[312,124,474,344,273,220,230,196,464,0,351,436,298,456,316,406,203,10,160,39,28,357,354,439,315,300,447,193,322,243,451,317,265,271,214,13,427,407,69,254,484,280,409,294,216,486,403,187,419,56,422,60,338,279,383,27,71,239,293,266,38,24,195,194,175,405,307,246,2,347,482,441,413,240,137,493,113,434,226,421,426,115,329,353,53,223,159,241,44,314,349,328,255,391,275,127,256,295,227,490,258,337,213]

for root, dirs, files in list_dirs:
    for file in files:
        if ('.txt'in file):#and title.replace(' ','_') in file):
            title=file.replace('_',' ').replace('.txt','')
            if int(title) not in selectindex:
                continue
            print(title)
            datapath=root+file
            rootmap =sc.textFile(datapath)

            def paphtweet(tweettext):
                tweet = {
                'tweet_id': 0,
                'text': None,
                'user_id': None,
                'user_screen_name': None,
                'user_name': None,
                'created_at': None,
                'retweets': 0,
                'favorites': 0,
                'isretweet':False,
                'retweet_from_userid':None,
                'retweet_from_tweetid':None,
                'contain_photos':False,
                'contain_photos_number':0,
                'contain_photos_url':list(),
                'contain_videos':False,
                'hashtags':list(),
                'menstion':list(),
                'urls':list()}
                tweet['tweet_id']=tweettext['id']
                tweet['text']=tweettext['text']
                tweet['user_id']=tweettext['user']['id']
                tweet['user_screen_name']=tweettext['user']['screen_name']
                tweet['user_name']=tweettext['user']['name']
                tweet['retweets']=tweettext['retweet_count']
                if "RT @" in tweet['text'] or "RT@" in tweet['text']or "RT" in tweet['text']:
                    tweet['isretweet']=True
                tweet['created_at']=tweettext['created_at']
                tweet['urls']=re.findall(r'(https?://\S+)', tweet['text'])
                tweet['hashtags']=re.findall(r'(#\S+)', tweet['text'])
                tweet['menstion']=re.findall(r'(@\S+)', tweet['text'])
                tweet['retweets']=tweettext['retweet_count']



            rootJSONMap=rootmap.map(lambda line2:(json.loads(line2))).map(lambda line2:(paphtweet(line2))).collect()

            with open(outputFile+'1'+title+'.txt', mode='w') as writer:
                for tweet in rootJSONMap:
                    JSON=json.dumps(tweet)
                    writer.write(JSON + '\n')
