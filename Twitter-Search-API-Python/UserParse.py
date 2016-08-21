from bs4 import BeautifulSoup
import path
import datetime
import json
import findspark
findspark.init(spark_home='/Applications/spark-1.6.1')
from pyspark import SparkContext, SparkConf
import os
import time

simpleuserlist=dict()
with open( path.USerJSONpath+'simple_'+'UserJson.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        simpleuserlist[int(data['user_id'])]=data

def getHtmlfromJson(jsontext):
    try:
      return json.loads(jsontext)["html"]
    except ValueError:
        return ''
    except TypeError:
        return ''

def getNumberFromStr(text):
    thou=False
    for i in range(10):
        substr=str(i)+'K'
        if text.find(substr) != -1:
            thou=True
            break

    numberstr='0123456789.'
    tempstr=text
    for char in text:
        if char not in numberstr:
            tempstr=tempstr.replace(char,'')
    if thou:
        return int(float(tempstr)*1000)
    else:
        return int(tempstr)

def parse_tweets(docusername,items_html):
        """
        Parses Tweets from the given HTML
        :param items_html: The HTML block with tweets
        :return: A JSON list of tweets
        """
        print(docusername)
        docusername=docusername.replace('.html','').split('/')[-1]
        try:
            soup = BeautifulSoup(items_html,"lxml")
        except TypeError:
            print(items_html)
        user = {
            'data-background-image': None,
            'user_id': None,
            'user_screen_name': None,
            'user_name': None,
            'followers_count': 0,
            'location':None,
            'friends_count':0,
            'favourites_count':0,
            'photos_count':0,
            'tweets_count':0,
            'Join_date':None,
            'Description':None,
            'hashtagsInDescription':list(),
            'menstionInDescription':list(),
            'urlsInDescription':list(),
            'url':None,
            'verified':False
        }
        # Tweet Text
        try:
            headcard = soup.find("div", class_="ProfileHeaderCard")
            if headcard is None:
                return None
            description=headcard.find('p','ProfileHeaderCard-bio u-dir')
            user['verified']=headcard.find('a',{'href','https://twitter.com/help/verified'}) is not None or headcard.find('a',{'title','Verified account'}) is not None or headcard.find('a',{'href','/help/verified'}) is not None

            if description is not None:
                user['Description'] = description.get_text()#.encode('utf-8')
                if description.find('a','twitter-hashtag pretty-link js-nav') is not None:
                    for hastag in description.find_all('a','twitter-hashtag pretty-link js-nav'):
                        user['hashtagsInDescription'].append(hastag.get_text())#.replace('data-image-url',''))
                if description.find('a','tweet-url twitter-atreply pretty-link') is not None:
                    for menstion in description.find_all('a','tweet-url twitter-atreply pretty-link'):
                        user['menstionInDescription'].append(menstion.get_text())
                if description.find('a','twitter-timeline-link') is not None:
                    for url in description.find_all('a','twitter-timeline-link'):
                        user['urlsInDescription'].append(url.get('title'))

            location=headcard.find('span','ProfileHeaderCard-locationText u-dir')
            if location is not None:
                user['location']=location.text.replace('\n','').strip(' ')
            joindate=headcard.find('span','ProfileHeaderCard-joinDateText js-tooltip u-dir')
            if joindate is not None:
                user['Join_date']=joindate.get('title')
            user['user_id']=int(soup.find('div','ProfileNav').get('data-user-id'))
            if user['user_id'] in simpleuserlist.keys():
                    user['verified']=simpleuserlist[user['user_id']]['verified']
            user['user_name']=headcard.find('h1','ProfileHeaderCard-name').find('a').text
            #user['user_name']=headcard.find('a','ProfileHeaderCard-nameLink u-textInheritColor js-nav\n').text
            user['user_screen_name']=headcard.find('a','ProfileHeaderCard-screennameLink u-linkComplex js-nav').text

            photos=soup.find("a", class_="PhotoRail-headingWithCount js-nav")
            if photos is not None:
                user['photos_count']=getNumberFromStr(photos.text)
            tweets_count=soup.find('a','ProfileNav-stat ProfileNav-stat--link u-borderUserColor u-textCenter js-tooltip js-nav')
            if tweets_count is not None:
                user['tweets_count']=getNumberFromStr(tweets_count.get('title'))
            followers_count=soup.find('a',{'data-nav':"followers"})
            if followers_count is not None:
                user['followers_count']=getNumberFromStr(followers_count.get('title'))
            friends_count=soup.find('a',{'data-nav':"following"})
            if friends_count is not None:
                user['friends_count']=getNumberFromStr(friends_count.get('title'))
            favourites_count=soup.find('a',{'data-nav':"favorites"})
            if favourites_count is not None :
                user['favourites_count']=getNumberFromStr(favourites_count.get('title'))

            # Tweet User ID, User Screen Name, User Name

            return user
        except AttributeError:
            print("wrong doc  "+docusername)
            raise  AttributeError






prck =False

if prck :
    conf = SparkConf().setMaster("local[4]").setAppName("Spark Count")
    sc = SparkContext(conf=conf)
    #

    datapath=path.userrawpath+'News/*.html'
    wordCounts = sc.wholeTextFiles(datapath).map(lambda doc: parse_tweets(doc[0],doc[1]))#.filter(lambda tweet:  tweet is not None)#.reduceByKey(lambda v1,v2:v1 +v2)

    for tweet in wordCounts.collect():
        with open( path.USerJSONpath+'nwUserJson.txt', encoding='utf-8', mode='a') as Seenlist:
            JSON = json.dumps(tweet, ensure_ascii=False)
            Seenlist.write(JSON + '\n')
#
else:
    wordCounts=list()
    names=list()
    list_dirs = os.walk(path.userrawpath+"News")
    for root, dirs, files in list_dirs:
        for d in files:
            if 'html' not in d or d[0] !='_':
                continue
    for tweet in wordCounts:
            with open( path.USerJSONpath+'2nwUserJson.txt', encoding='utf-8', mode='a') as Seenlist:
                JSON = json.dumps(tweet, ensure_ascii=False)
                Seenlist.write(JSON + '\n')
#
#with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/User_RAW/Evil_Woody.html', encoding='utf-8', mode='r') as Seenlist:

 #  parse_tweets(Seenlist)