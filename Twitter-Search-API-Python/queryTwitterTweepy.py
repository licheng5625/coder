
import time
import tweepy

auth = tweepy.OAuthHandler('V0dszSPR1da4exOnePoPV2spF', 'ahpHyWeiwH2ebOAIrJD3wm1NYlFyXp3JEe7uCCap5UC3qqoK7c')
auth.set_access_token('114177663-k84mzvQyg3LVz9Fs4KGk70RveLaUtk7L1r4SfagF', 'rcg7EChRmeFemrChegWqy8jRt3tieMwHGCzvXGCd9DMk9')

api = tweepy.API(auth)

def execute_search(self, url,counter=0):
        """
        Executes a search to Twitter for the given URL
        :param url: URL to search twitter with
        :return: A JSON object with data from Twitter
        """
        counter=counter+1
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
            print(("Sleeping for %i" % self.error_delay))
            sleep(self.error_delay)
            if counter<5:
                return self.execute_search(url,counter)
            else:
                raise BlacklistError()

        except urllib.error.HTTPError as e:
            print(headers['user-agent'])
            print(e.reason)
            if counter<5:
                return self.execute_search( url,counter)
            else:
                raise BlacklistError()
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(2 * 60)

for follower in limit_handled(tweepy.Cursor(api.friends,id='114177663',count=5000).pages()):
      print ((follower))
# i=0
# for follower in limit_handled(tweepy.Cursor(api.search,q = ' Ammon Bundy Rosa Parks',count=100).items()):
#     print (follower)
#     i=i+1
# print(i)


# pubic_tweets = api.retweeters(id='746573395030999040',count=100)
# print(pubic_tweets)
# for tweet in pubic_tweets:
#     print (tweet)
# print(len(pubic_tweets))
# print('114177663' in pubic_tweets)