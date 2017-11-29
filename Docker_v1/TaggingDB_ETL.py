#-*- coding:utf-8 -*-
import inspect
import os
import redis
import pandas as pd
import numpy as np
import sys
from datetime import datetime
import time
import json
redis_ip = 'localhost'
reload(sys)
sys.setdefaultencoding('utf8')

# Read Data
file_path = inspect.getfile(inspect.currentframe())
file_direction = os.path.dirname(os.path.abspath(file_path))

file_path_tag = os.path.join( file_direction , 'Tag_DB.json' )
file_path_db = os.path.join( file_direction , 'Tagging_Db_test.xlsx' )

tagdb_file = open(file_path_tag, 'r')
df = pd.read_excel(file_path_db)
tagdb_file
TAG_DB  = json.load(tagdb_file)

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


# 貼標
def Tag_query(DB, tag):
    for i in DB:
        if i['TAG_ID'] == tag:
            tag = {}
            tag['TAG_ID'] = i['TAG_ID']
            tag['scenario'] = i['scenario']
            tag['dataSource'] = i['dataSource']
            tag['securityFilter'] = i['securityFilter']
            tag['expireTime'] =  i['expireAfter']
            tag['isValid'] = i['isActive']
            return tag


# 組裝Tagging_Db，並塞入DB
def TaggingDB_ETL(data,TagDB ):
    # Redis設定
    conn = redis.Redis(host=redis_ip,port=6379,db=0)
    vids = data.VID.unique()
    for i in vids:
        Tagging_DB = {}
        Tagging_DB['VID'] = i
        Tagging_DB['batchTag'] = []
        Tagging_DB['realtimeTag'] = []
        tag = data[data.VID==i]['TAG_ID'].values
        for j in range(len(tag)):
            Tagging_DB['batchTag'].append(Tag_query(TagDB, tag[j]))
            tagtime_obj =  datetime.strptime(df[(df.VID==i) & (df.TAG_ID==tag[j])].TAGTIME.values[0], '%Y/%m/%d:%H:%M:%S')
            tagtime_obj = time.mktime(tagtime_obj.timetuple())
            Tagging_DB['batchTag'][j]['tagTime'] = tagtime_obj
            Tagging_DB['batchTag'][j]['expireTime'] += Tagging_DB['batchTag'][j]['tagTime']
        conn.set(i, json.dumps(Tagging_DB,ensure_ascii=False))

# 把資料送進DB
TaggingDB = TaggingDB_ETL(df, TAG_DB)
