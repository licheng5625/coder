import mypath as path
import json
descriptionFile=path.TweetJSONpath+'descriptionNews.txt'
eventid=[]
evtcod={}
with open(descriptionFile,encoding='utf-8', mode='r')as Seenlist2:
    for line in Seenlist2:
        # print(line)
        data=json.loads(line)
        eventid.append( data['eventID']-1000)


with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Feature/event_categories.tsv',encoding='utf-8', mode='r')as Seenlist22:
    for line2 in Seenlist22:
        evtid =int(line2.split('	')[0])
        if evtid in eventid:
            try:
                evtcod[line2.split('	')[1]]= evtcod[line2.split('	')[1]]+1
            except KeyError:
                evtcod[line2.split('	')[1]]= 1
for ke in evtcod.keys():
    print(ke)
    print(evtcod[ke])