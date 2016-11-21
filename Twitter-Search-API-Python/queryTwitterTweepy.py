
import time
import tweepy
import urllib
import zlib
from bs4 import BeautifulSoup
import mypath
import json

auth = tweepy.OAuthHandler('V0dszSPR1da4exOnePoPV2spF', 'ahpHyWeiwH2ebOAIrJD3wm1NYlFyXp3JEe7uCCap5UC3qqoK7c')
auth.set_access_token('114177663-k84mzvQyg3LVz9Fs4KGk70RveLaUtk7L1r4SfagF', 'rcg7EChRmeFemrChegWqy8jRt3tieMwHGCzvXGCd9DMk9')

api = tweepy.API(auth)

filename=mypath.TweetJSONpath+'usersrumors.txt'
outfile=mypath.USerJSONpath+'UserjsonNew.txt'
userset=set()
with open(filename,mode='r')as er:
    for line in er:
        userset.add(int(line))
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

def getData(username):
        opener = urllib.request.build_opener()
        # if len(self.header) ==0:
        #     self._getHeader()
        opener.addheaders =[('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
        url=opener.open('https://twitter.com/'+username).read()
        return zlib.decompress(url, 16+zlib.MAX_WBITS)
craweduser=set()
def saveUser(userlist):
    for follower in api.lookup_users( user_ids=userlist):
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
                timeformate='%I:%M %p - %d %b %Y'

                user['user_id']=follower.id
                user['user_screen_name']=follower.screen_name
                user['user_name']=follower.name
                user['followers_count']=follower.followers_count
                user['location']=follower.location
                user['friends_count']=follower.friends_count
                user['favourites_count']=follower.followers_count
                user['tweets_count']=follower.statuses_count
                user['Join_date']=follower.created_at.strftime(timeformate)
                user['Description']=follower.description
                user['verified']=follower.verified
                html=getData(follower.screen_name)
                soup = BeautifulSoup(html,"lxml")
                photos=soup.find("a", class_="PhotoRail-headingWithCount js-nav")
                if photos is not None:
                    user['photos_count']=getNumberFromStr(photos.text)
                with open (outfile,mode='a')as reader:
                    reader.write(json.dumps(user)+'\n')
with open (outfile,encoding='utf-8',mode='r')as reader:
    for line in reader:
        user=json.loads(line)
        craweduser.add(user['user_id'])
tempidlist=[]
for userid in userset:
    if userid not in craweduser:
        tempidlist.append(userid)
    if len(tempidlist)==100:
        saveUser(tempidlist)
        tempidlist=[]
saveUser(tempidlist)


