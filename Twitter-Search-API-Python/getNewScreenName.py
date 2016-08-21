import path
import urllib.request, urllib.error, urllib.parse
import json
import datetime
from abc import ABCMeta
from urllib.parse import urlencode
from abc import abstractmethod
from urllib.parse import urlunparse
from bs4 import BeautifulSoup
from time import sleep


class BlacklistError(Exception):
    def __init__(self):
        return

def execute_search( url,counter=0):
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
            headers['user-agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read().decode('utf-8'))
            return data

        # If we get a ValueError exception due to a request timing out, we sleep for our error delay, then make
        # another attempt
        except ValueError as e:
            print(("Sleeping for %i" % 2))
            sleep(2)
            if counter<5:
                return execute_search(url,counter)
            else:
                return None

        except urllib.error.HTTPError as e:
            #print(headers['user-agent'])
            #print(e.reason)
            if counter<5:
                return execute_search( url,counter)
            else:
                return None


def construct_url(query, max_position=None):
        """
        For a given query, will construct a URL to search Twitter with
        :param query: The query term used to search twitter
        :param max_position: The max_position value to select the next pagination of tweets
        :return: A string URL
        """

        params = {
            # Type Param
            'user_id': query,
            #'f': 'tweets',
            # Query Param
        }

        # If our max_position param is not None, we add it to the parameters
#https://twitter.com/i/profiles/popup?user_id=263253968&wants_hovercard=true&_=1467635602769
        url_tupple = ('https', 'twitter.com', '/i/profiles/popup', '', urlencode(params), '')
        return urlunparse(url_tupple)

userlist=dict()
blackuserid=list()
searchedblackuserid=set()
with open(path.userrawpath+'usersnews.txt', mode='r')as Seenlist2:
    for line in Seenlist2:
        line=line.replace('\n','')
        id=line.split('  ')[1]
        userid=line.split('  ')[0]
        userlist[id]=userid
with open(path.userrawpath+'blacklistnews.txt', mode='r')as Seenlist2:
    for line in Seenlist2:
        line=line.replace('\n','')
        newid=userlist[line]
        blackuserid.append(newid)
# with open(path.userrawpath+'seachedblacklist.txt', mode='r')as Seenlist2:
#     for line in Seenlist2:
#         line=line.replace('\n','')
#         searchedblackuserid.add(line)


for userid in blackuserid :
    if  userid not in searchedblackuserid:
        url=construct_url(userid)
        response  = execute_search(url)
        if response is not None  :
            newscreenname=response['screen_name']
            with open(path.userrawpath+'addlist.txt', mode='a')as Seenlist2:
                Seenlist2.write(newscreenname+'\n')
            with open(path.userrawpath+'seachedblacklist.txt', mode='a')as Seenlist2:
                Seenlist2.write(userid+'\n')