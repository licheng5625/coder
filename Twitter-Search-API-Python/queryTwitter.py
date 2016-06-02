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


output = client.api.search.tweets.get(q = '((apple OR apples ) AND cancer)  (Caused OR Cause OR Causes OR wax OR waxed)',count ='1000',f='tweets')
#output = client.api.search.tweets.get(q = 'apple')
print output
print output.data