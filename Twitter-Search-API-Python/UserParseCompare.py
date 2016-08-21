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
with open( path.USerJSONpath+'UserJson.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        comuserlist[int(data['user_id'])]=data
with open( path.USerJSONpath+'nwUserJson.txt', encoding='utf-8', mode='r') as Seenlist:
    for line in Seenlist:
        data=json.loads(line.replace('\n',''))
        comuserlist[int(data['user_id'])]=data
for sim in simpleuserlist.keys():
    if sim not in comuserlist.keys():
        with open( path.USerJSONpath+'lessID.txt', encoding='utf-8', mode='a') as Seenlist:
            Seenlist.write(str(sim)+'   '+simpleuserlist[sim]['screen_name']+'\n')