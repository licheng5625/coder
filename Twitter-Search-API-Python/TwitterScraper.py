import urllib.request, urllib.error, urllib.parse
import json
import datetime
from abc import ABCMeta
from urllib.parse import urlencode
from abc import abstractmethod
from urllib.parse import urlunparse
from bs4 import BeautifulSoup
from time import sleep
import path
import random
import os
from fake_useragent import UserAgent

__author__ = 'Tom Dickinson'


class TwitterSearch(metaclass=ABCMeta):

    def __init__(self,projectname, rate_delay,error_delay=5):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        """
        self.ua = UserAgent()

        self.projectname=projectname
        self.rate_delay = rate_delay
        self.error_delay = error_delay
    def search(self, query):
        """
        Scrape items from twitter
        :param query:   Query to search Twitter with. Takes form of queries constructed with using Twitters
                        advanced search: https://twitter.com/search-advanced
        """
        url = self.construct_url(query)
        continue_search = True
        min_tweet = None
        response  = self.execute_search(url)
        while response is not None and continue_search and response['items_html'] is not None:
            tweets = self.parse_tweets(response['items_html'])

            # If we have no tweets, then we can break the loop early
            if len(tweets) == 0:
                break

            # If we haven't set our min tweet yet, set it now
            if min_tweet is None:
                min_tweet = tweets[0]

            continue_search = self.save_tweets(tweets)
            # Our max tweet is the last tweet in the list
            max_tweet = tweets[-1]
            self.save_webpage(response)
            if min_tweet['tweet_id'] is not max_tweet['tweet_id']:
                max_position = "TWEET-%s-%s" % (max_tweet['tweet_id'], min_tweet['tweet_id'])
                url = self.construct_url(query, max_position=max_position)
                # Sleep for our rate_delay
                sleep(self.rate_delay)
                response = self.execute_search(url)

    def execute_search(self, url):
        """
        Executes a search to Twitter for the given URL
        :param url: URL to search twitter with
        :return: A JSON object with data from Twitter
        """

        try:
            # Specify a user agent to prevent Twitter from returning a profile card
            headers = {
                'user-agent': None
            }
            headers['user-agent']=self.ua.random
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            return data

        # If we get a ValueError exception due to a request timing out, we sleep for our error delay, then make
        # another attempt
        except ValueError as e:
            print((e.message))
            print(("Sleeping for %i" % self.error_delay))
            sleep(self.error_delay)
            return self.execute_search(url)
        except urllib.error.HTTPError:
            print('error')
            print(headers['user-agent'])
            return self.execute_search( url)

    @staticmethod
    def parse_tweets(items_html):
        """
        Parses Tweets from the given HTML
        :param items_html: The HTML block with tweets
        :return: A JSON list of tweets
        """
        soup = BeautifulSoup(items_html, "html")
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
                'favorites': 0
            }

            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text().encode('utf-8')

            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-user-id']
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

    @staticmethod
    def construct_url(query, max_position=None):
        """
        For a given query, will construct a URL to search Twitter with
        :param query: The query term used to search twitter
        :param max_position: The max_position value to select the next pagination of tweets
        :return: A string URL
        """

        params = {
            # Type Param
            #'f': 'all',
            'f': 'tweets',
            # Query Param
            'q': query
        }

        # If our max_position param is not None, we add it to the parameters
        if max_position is not None:
            params['max_position'] = max_position

        url_tupple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
        return urlunparse(url_tupple)

    @abstractmethod
    def save_tweets(self, tweets):
        """
        An abstract method that's called with a list of tweets.
        When implementing this class, you can do whatever you want with these tweets.
        """

    @abstractmethod
    def save_webpage(self, pages):
        """
        An abstract method that's called with a list of tweets.
        When implementing this class, you can do whatever you want with these tweets.
        """
class TwitterSearchImpl(TwitterSearch):

    def __init__(self,projectname, rate_delay, error_delay, max_tweets):
        """
        :param rate_delay: How long to pause between calls to Twitter
        :param error_delay: How long to pause when an error occurs
        :param max_tweets: Maximum number of tweets to collect for this example
        """
        super(TwitterSearchImpl, self).__init__(projectname,rate_delay, error_delay)
        self.max_tweets = max_tweets
        self.counter = 0
        self.projeckDir=path.datapath+'webpagefortwitter/'+self.projectname+'/'
    def count_tweets(self, tweets):
        return len(tweets)
    def save_tweets(self, tweets):
        """
        Just prints out tweets
        :return:
        """
        if os.path.isdir(self.projeckDir.lstrip('/')):
            pass
        else:
            os.mkdir(self.projeckDir.rstrip('/'))
        for tweet in tweets:
            # Lets add a counter so we only collect a max number of tweets
            self.counter += 1

            if tweet['created_at'] is not None:
                t = datetime.datetime.fromtimestamp((tweet['created_at']/1000))
                fmt = "%Y-%m-%d %H:%M:%S"
                print(("%i [%s] - %s" % (self.counter, t.strftime(fmt), tweet['text'])))
                fmt="%Y-%m-%d"
                with open( self.projeckDir+self.projectname+'.txt', encoding='utf-8', mode='a') as Seenlist:
                    Seenlist.write(t.strftime(fmt) +'   '+(tweet['text']).decode('utf-8')+'\n')
            # When we've reached our max limit, return False so collection stops
            if self.counter >= self.max_tweets:
                return False

        return True

    def save_webpage(self, pages):

        with open( self.projeckDir+self.projectname+str(self.counter)+'.txt', encoding='utf-8', mode='w') as Seenlist:
            JSON = json.dumps(pages, ensure_ascii=False)
            Seenlist.write(JSON + '\n')


if __name__ == '__main__':
    checkedlist=list()
    with open(  path.datapath+"checkedRumorsLIST.txt", mode='r') as Seenlist2:
        for sentence in   Seenlist2:
            checkedlist.append(sentence.replace('\n',''))

    with open(  path.datapath+"checkedRumorsLIST.txt", mode='a') as Seenlist2:
        with open(  path.datapath+"RumorsLIST.txt", mode='r') as Seenlist:
            for sentence in Seenlist:
                checkedtitle=sentence.split("@,@")[1].replace('\n','')
                if(checkedtitle not in checkedlist):
                    twit = TwitterSearchImpl(checkedtitle,1, 5, 1500000)
                    twit.search(sentence.split("@,@")[0])
                    checkedlist.append(checkedtitle)
                    Seenlist2.write(checkedtitle+'\n')

    #twit.search("Huggies AND（Glass OR glasses OR fiberglass) AND (Wipes OR wipe) ")
    #twit.search("(Olive Garden) ( Planned Parenthood)  ")
    #twit.search("(recharge OR charge OR charging) (microwave OR microwaving OR \"microwave oven\") (phone OR phones OR iphone) ")
    #twit.search("twitter summize   (buy OR buys OR bought OR Purchase)")
    #twit.search("(wax OR waxed OR waxing OR youtu.be/X2K1WSqlP4o  ) (apple OR apples) (cancer) ")
    #twit.search("(banana OR bananas) (HIV OR  AIDS)   (infected OR Infected ) ")

