from bs4 import BeautifulSoup
import mypath as path
import datetime
import json
import findspark
findspark.init(spark_home='/Applications/spark-1.6.1')
from pyspark import SparkContext, SparkConf
import os


def getHtmlfromJson(jsontext):
    try:
      return json.loads(jsontext)["items_html"]
    except ValueError:
        return ''
    except TypeError:
        return ''

def parse_tweets(items_html):
        """
        Parses Tweets from the given HTML
        :param items_html: The HTML block with tweets
        :return: A JSON list of tweets
        """
        try:
            soup = BeautifulSoup(items_html)
        except TypeError:
            print(items_html)
        tweets = []
        for li in soup.find_all("li", class_='js-stream-item'):

            # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
            if 'data-item-id' not in li.attrs:
                continue

            tweet = {
                'tweet_id': li['data-item-id'],
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
                'urls':list()
            }
            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()#.encode('utf-8')
            if ("RT @" in tweet['text'] or "RT@" in tweet['text']or "RT" in tweet['text']) and li.find('a','twitter-atreply pretty-link js-nav') is not None:
                tweet['isretweet']=True
                tweet['retweet_from_userid']=li.find('a','twitter-atreply pretty-link js-nav').get('data-mentioned-user-id')
                #print (tweet['retweet_from_userid'])

            if li.find('div',"QuoteTweet-innerContainer u-cf js-permalink js-media-container") is not None and li.find('div',"QuoteTweet-innerContainer u-cf js-permalink js-media-container").get('data-item-type') == 'tweet':
                tweet['isretweet']=True
                tweet['retweet_from_userid']=li.find('div',"QuoteTweet-innerContainer u-cf js-permalink js-media-container").get('data-user-id')
                tweet['retweet_from_tweetid']=li.find('div',"QuoteTweet-innerContainer u-cf js-permalink js-media-container").get('data-item-id')

            if li.find('div',"AdaptiveMedia-singlePhoto") is not None:
                tweet['contain_photos_number']=1
                tweet['contain_photos_url'].append(li.find('div','AdaptiveMedia-photoContainer js-adaptive-photo ').get('data-image-url'))
                tweet['contain_photos']=True


            if li.find('div',"AdaptiveMedia-doublePhoto") is not None:
                tweet['contain_photos_number']=2
                tweet['contain_photos']=True

                picturescontainer=li.find('div',"AdaptiveMedia-doublePhoto")
                for threephoto in picturescontainer.find_all('div','AdaptiveMedia-photoContainer js-adaptive-photo'):
                    tweet['contain_photos_url'].append(threephoto.get('data-image-url'))
            if li.find('div',"AdaptiveMedia-triplePhoto") is not None:
                tweet['contain_photos_number']=3
                tweet['contain_photos']=True
                picturescontainer=li.find('div',"AdaptiveMedia-triplePhoto")
                for threephoto in picturescontainer.find_all('div','AdaptiveMedia-photoContainer js-adaptive-photo '):
                    tweet['contain_photos_url'].append(threephoto.get('data-image-url'))
            if li.find('div',"AdaptiveMedia-quadPhoto") is not None:
                tweet['contain_photos_number']=4
                picturescontainer=li.find('div',"AdaptiveMedia-quadPhoto")
                #tweet['contain_photos_url'].append(li.find('div','AdaptiveMedia-photoContainer js-adaptive-photo').get('data-image-url'))
                for threephoto in picturescontainer.find_all('div','AdaptiveMedia-photoContainer js-adaptive-photo '):
                    tweet['contain_photos_url'].append(threephoto.get('data-image-url'))

            if li.find('div',"AdaptiveMedia-video") is not None or li.find('div',"Nonejs-macaw-cards-iframe-container card-type-player") is not None:
                tweet['contain_videos']=True
            if li.find('a','twitter-atreply pretty-link js-nav') is not None:
                for menstion in li.find_all('a','twitter-atreply pretty-link js-nav'):
                    tweet['menstion'].append(menstion.get('data-mentioned-user-id'))
            if li.find('a','twitter-hashtag pretty-link js-nav') is not None:
                for hastag in li.find_all('a','twitter-hashtag pretty-link js-nav'):
                    tweet['hashtags'].append(hastag.get_text('data-image-url').replace('data-image-url',''))
            if li.find('a','twitter-timeline-link') is not None:
                for link in li.find_all('a','twitter-timeline-link'):
                    title =link.get('title')
                    if title is not None:
                        tweet['urls'].append(title)


            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-screen-name']
                tweet['user_name'] = user_details_div['data-name']

            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = float(date_span['data-time-ms'])

            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])

            # Tweet Favourites
            favorite_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if favorite_span is not None and len(retweet_span) > 0:
                tweet['favorites'] = int(favorite_span[0]['data-tweet-stat-count'])

            tweets.append(tweet)
        return tweets
def selectone(v1,v2):
    return v1
test=False

if test:

    conf = SparkConf().setAppName("Spark Count")
    sc = SparkContext(conf=conf)


    list_dirs = os.walk(path.datapath+'/webpagefortwitter/Tweet_RAW/rumorsnopes/')
    for root, dirs, files in list_dirs:
        for d in dirs:

            folder=os.path.join(root, d)
            print(folder)
            datapath=folder+'/*.txt'
            wordCounts = sc.textFile(datapath).flatMap(lambda doc: parse_tweets(getHtmlfromJson(doc)))#.flatMap(lambda tweet: parse_tweets(tweet))#.reduceByKey(lambda v1,v2:v1 +v2)
            for tweet in wordCounts.collect():
                with open( path.TweetJSONpath+'rumorsnopes/'+d+'.txt', encoding='utf-8', mode='a') as Seenlist:
                    JSON = json.dumps(tweet, ensure_ascii=False)
                    Seenlist.write(JSON + '\n')
else:

    with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_RAW/News/halfbro/halfbro685.txt',encoding='utf-8',mode='r') as ss:
         print(parse_tweets(getHtmlfromJson(ss.read())))

    conf = SparkConf().setAppName("Spark Count")
    sc = SparkContext(conf=conf)

    d='munich'
    datapath =  (path.datapath+'/webpagefortwitter/Tweet_RAW/News/munich/*.txt')
    wordCounts = sc.textFile(datapath).flatMap(lambda doc: parse_tweets(getHtmlfromJson(doc))).map(lambda tweet:(tweet['tweet_id'],tweet)).reduceByKey(lambda v1,v2:selectone(v1 ,v2)).map(lambda tweet:(int(tweet[1]['created_at']),tweet[1]))\
                .sortByKey(True).map(lambda tweet: tweet[1])
    for tweet in wordCounts.collect():
        with open( path.TweetJSONpath+'news/'+d+'.txt', encoding='utf-8', mode='a') as Seenlist:
            JSON = json.dumps(tweet, ensure_ascii=False)
            Seenlist.write(JSON + '\n')


#with open(  path.datapath+"/webpagefortwitter/banana HIV/banana HIV470.txt", mode='r') as Seenlist2:
  #      jsonoftweet=getHtmlfromJson(Seenlist2.read())
#        print(parse_tweets(jsonoftweet["items_html"]))