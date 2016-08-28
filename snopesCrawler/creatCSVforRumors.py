filepath='/Users/licheng5625/PythonCode/masterarbeit/data/jounral.txt'
import json
import random
import datetime
import csv
def clearText(strs):
    ret= strs.replace('—','').replace(' ','').lstrip(':').lstrip(' ')
    return ret

counter=0
rumorslist=[]
def byTime_key(rumor):
    return datetime.datetime.strptime(rumor['Originally published Time'],"%d %B %Y")

with open(filepath,encoding='utf-8',mode='r')as rumors:
    for line in rumors:
        counter+=1
        JSON=json.loads(line)
        rumorslist.append(JSON)
rumorslist=[elem for elem in rumorslist if 'Originally published Time' in elem.keys() and 'Result' in elem.keys() ]
random.shuffle(rumorslist)
checkedrumor=set()
with open('/Users/licheng5625/PythonCode/masterarbeit/data/rumorCSV/MixtureCSV.csv', 'w') as csvfilemix:
    fieldnames = ['link', 'Tags','Headline','Claim','Description','Originally published Time','Result','Query','Difficulty level']
    writermix = csv.DictWriter(csvfilemix, fieldnames=fieldnames)
    writermix.writeheader()

    for i in range(0,len(rumorslist),int(len(rumorslist)/10)):
            if i+int(len(rumorslist)/10)*2>len(rumorslist):
                rumorssubset=rumorslist[i:]
            else:
                rumorssubset=rumorslist[i:i+int(len(rumorslist)/10)]
            rumorssubset.sort(key=byTime_key,reverse=True)
            with open('/Users/licheng5625/PythonCode/masterarbeit/data/rumorCSV/rumorsCSV'+str(i)+'.csv',encoding='utf-8', mode='w') as csvfile:

                #fieldnames = ['link', 'Tags','Headline','Claim','Description','Originally published Time','Result']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for rumor in rumorssubset:
                    if rumor['Result']=='FALSE' and rumor['link'] not in checkedrumor:
                        tags=''
                        for tag in rumor['Tags']:
                            tags=tag+'    '
                        writer.writerow({'link': 'http://www.snopes.com'+rumor['link'],
                                         'Tags': rumor['Tags'],
                                         'Headline': clearText(rumor['headline']),
                                         'Claim': clearText(rumor['Claim']),
                                         'Description': clearText(rumor['description']),
                                         'Originally published Time': rumor['Originally published Time'],
                                         'Result': 'FALSE',
                                         })
                    if rumor['Result']=='MIXTURE' and rumor['link'] not in checkedrumor:
                        tags=''
                        for tag in rumor['Tags']:
                            tags=tag+'    '
                        writermix.writerow({'link': 'http://www.snopes.com'+rumor['link'],
                                     'Tags': rumor['Tags'],
                                     'Headline': rumor['headline'].replace(' ',''),
                                     'Claim': rumor['Claim'].replace(' ',''),
                                     'Description': rumor['description'].replace(' ',''),
                                     'Originally published Time': rumor['Originally published Time'],
                                     'Result': 'MIXTURE',
                                     })
                    checkedrumor.add(rumor['link'])
