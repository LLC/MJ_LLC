#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json
import inspect
import inspect
import operator
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

file_path = inspect.getfile(inspect.currentframe())
file_direction = os.path.dirname(os.path.abspath(file_path))

file_path_interest = os.path.join( file_direction , 'INTEREST_TAG.xlsx' )
file_path_intent = os.path.join( file_direction , 'INTENT_TAG.xlsx' )
file_path_db = os.path.join( file_direction , 'Tagging_Db.xlsx' )

Interest = pd.read_excel(file_path_interest)
Intent = pd.read_excel(file_path_intent)
df = pd.read_excel(file_path_db)

TAG = Interest.append(Intent)
TAG = TAG.reset_index()

# TagDB 轉 JSON 檔
def TagDb_ETL(data):
    Tag_DB = []
    rows = len(data)
    for row in range(rows):
        Tag = {}
        Tag['TAG_ID'] = data['TAG_ID'][row]
        Tag['scenario'] = {'DIIS1' : '',
                          'DIIS2' : '',
                          'DIIS3' : ''}
        scenario = data.scenario[row].split('|')
        for j in range(len(scenario)):
            DIIS = 'DIIS' + str(j+1)
            Tag['scenario'][DIIS] = scenario[j]
        Tag['recommedWeight'] = data['recommedWeight'][row]
        Tag['modelId'] = data['modelId'][row]
        Tag['operationType'] = data['operationType'][row]
        Tag['dataSource'] = data['dataSource'][row]
        Tag['securityFilter'] = data['securityFilter'][row]
        Tag['expireAfter'] = data['expireAfter'][row]
        Tag['createTime'] = data['create Time'][row]
        Tag['updateTime'] = data['update Time'][row]
        Tag['tagVersion'] = data['tagVersion'][row]
        Tag['isActive'] = data['isActive'][row]
        Tag['Chinese_Desc'] = data['Chinese_Desc'][row]
        Tag['referenceDocument'] = data['referenceDocument'][row]
        Tag_DB.append(Tag)
    return Tag_DB

# 標籤庫Dict
TagDB = TagDb_ETL(TAG)

# 標籤庫寫出去存成Json
with open('Tag_DB.json','w') as outfile:
    outfile.write('[')
    for i in range(len(TagDB)-1):
        a = json.dumps(TagDB[i],ensure_ascii=False).encode('utf-8')
        outfile.write(a + ',')
    outfile.write(json.dumps(TagDB[len(TagDB)-1],ensure_ascii=False).encode('utf-8') + ']')

# 貼標
def Tag_query(DB, tag):
    for i in DB:
        if i['TAG_ID'] == tag:
            tag = {}
            tag['TAG_ID'] = i['TAG_ID']
            tag['scenario'] = i['scenario']
            tag['dataSource'] = i['dataSource']
            tag['securityFilter'] = i['securityFilter']
            tag['tagTime'] = time.time()
            tag['expireTime'] = time.time() + i['expireAfter']
            tag['isValid'] = i['isActive']
            return tag

# Tagging_Db
def Json_ETL(data):
    Tagging_DB = []
    vids = data.VID.unique()
    for i in vids:
        vid = {}
        vid['VID'] = i
        vid['batchTag'] = []
        vid['realtimeTag'] = []
        tag = data[data.VID==i]['TAG_ID']
        for j in tag:
            vid['batchTag'].append(Tag_query(TagDB, j))
        Tagging_DB.append(vid)
    return Tagging_DB

# Tagging_DB
Tagging = Json_ETL(df)

# 標籤庫寫出去存成Json
with open('Tagging_DB.json','w') as outfile:
    outfile.write('[')
    for i in range(len(Tagging)-1):
        a = json.dumps(Tagging[i],ensure_ascii=False).encode('utf-8')
        outfile.write(a + ',')
    outfile.write(json.dumps(Tagging[len(Tagging)-1],ensure_ascii=False).encode('utf-8') + ']')
