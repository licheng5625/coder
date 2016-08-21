__author__ = 'licheng5625'
from birdy.twitter import UserClient
import json
class MyClient(UserClient):
    @staticmethod
    def get_json_object_hook(data):
        return data

client = MyClient("V0dszSPR1da4exOnePoPV2spF",
        "ahpHyWeiwH2ebOAIrJD3wm1NYlFyXp3JEe7uCCap5UC3qqoK7c",
        "114177663-k84mzvQyg3LVz9Fs4KGk70RveLaUtk7L1r4SfagF",
        "rcg7EChRmeFemrChegWqy8jRt3tieMwHGCzvXGCd9DMk9")


output = client.api.search.tweets.get(q = '(obama OR USA) appreciation month  (-Military -Jazz)',count=100,until='2013-09-28')
#output = client.api.statuses.retweeters.ids.get(id = '746783589312888832')
for tweet in  output.data['statuses']:
    print(tweet)
#print(len(output.data ))
print(len(output.data['statuses']))