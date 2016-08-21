from bs4 import BeautifulSoup
import path
import datetime
import json
import findspark
findspark.init(spark_home='/Applications/spark-1.6.1')
from pyspark import SparkContext, SparkConf
import os
import time
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

        data = json.loads(items_html)
        user={
            'screen_name':"",
            'user_id':0,
            'verified':False
        }
        user['screen_name']=data['screen_name']
        user['user_id']=data['user_id']
        user['verified']= 'verified' in items_html
        return user

conf = SparkConf().setMaster("local[4]").setAppName("Spark Count")
sc = SparkContext(conf=conf)



list_dirs = os.walk(path.userrawpath+'News/')
for root, dirs, files in list_dirs:
    for d in dirs:
        if 'NewsRawSimple2' not in d :
            continue
        folder=os.path.join(root, d)


        #
        print(d)
        datapath=folder+'/*.txt'
        wordCounts = sc.wholeTextFiles(datapath).map(lambda doc: parse_tweets(doc[0],doc[1])).filter(lambda tweet:  tweet is not None)#.reduceByKey(lambda v1,v2:v1 +v2)


        for tweet in wordCounts.collect():
            with open( path.USerJSONpath+'simple_News_'+'UserJson2.txt', encoding='utf-8', mode='a') as Seenlist:
                JSON = json.dumps(tweet, ensure_ascii=False)
                Seenlist.write(JSON + '\n')
#


#with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/User_RAW/Evil_Woody.html', encoding='utf-8', mode='r') as Seenlist:

 #  parse_tweets(Seenlist)