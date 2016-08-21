import path
import datetime
import json
import findspark
findspark.init(spark_home='/Applications/spark-1.6.1')

import os
simpleuserlist= dict()
comuserlist=dict()
with open( path.USerJSONpath+'simple_'+'UserJson.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        simpleuserlist[int(data['user_id'])]=data
with open( path.USerJSONpath+'User_JSON.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        comuserlist[int(data['user_id'])]=data
with open( path.USerJSONpath+'UserJsonNews_new.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        if len(line)<2:
            continue
        try :
            data=json.loads(line.replace('\n',''))
            comuserlist[int(data['user_id'])]=data
        except Exception as e:
            print(line)
            raise e
with open( path.USerJSONpath+'UserJsonNews.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        comuserlist[int(data['user_id'])]=data

for sim in comuserlist.keys():
    if sim in simpleuserlist.keys():
        comuserlist[sim]['verified']=simpleuserlist[sim]['verified']

for sim in comuserlist.keys():
    with open( path.USerJSONpath+'merge.txt', encoding='utf-8', mode='a') as Seenlist:
        Seenlist.write(json.dumps(comuserlist[sim], ensure_ascii=False)+'\n')