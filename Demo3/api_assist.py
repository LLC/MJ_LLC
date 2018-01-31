#-*- coding:utf-8 -*-
import os
import sys
import json
import operator
from flask import Flask,g
import time
import pandas as pd
import numpy as np
from flask import jsonify
import json
import redis
from flask import request
import psycopg2

ip = 'redis'
reload(sys)
sys.setdefaultencoding('utf8')

r0 = redis.Redis(host=ip, port=6379, db=0) #輸入VID會回傳VID,batchTag和realtimeTag
r1 = redis.Redis(host=ip, port=6379, db=1) #輸入TagValue會回傳offer_list

table1 = pd.read_excel("TAG_LOG_DOWNLOAD.xlsx")
table1['TAG_VALUE'] = ""
table2 = pd.read_excel("TAG_Value_DOWNLOAD.xlsx")
table_merge = pd.concat([table1.loc[:,:], table2.loc[:,:]], axis = 0)
table_merge = table_merge.reset_index(drop=True)


# connect PostgreSQL
database='postgres'
host = 'postgres'
user = 'postgres'
password = ''

conn = psycopg2.connect(database = database,
                        host = host,
                        user = user,
                        password = password)

cur = conn.cursor()

def tag_db_query(UTID, sql_db):
    SQL = "SELECT tag_info FROM intent_db WHERE tag_info->>'TAG_ID' = '{}';".format(UTID)
    sql_db.execute(SQL)
    records = sql_db.fetchall()[0][0]
    return records

def offer_db_query(TAG_VALUE, sql_db):
    SQL = "SELECT tag_info FROM offer_db WHERE tag_info->>'tag_value' = '{}';".format(TAG_VALUE)
    sql_db.execute(SQL)
    records = sql_db.fetchall()[0][0]
    return records

unique_ID = np.unique(table_merge['ID'])
for i in unique_ID:
    temp_list = []
    temp_detail = {}    
    unique_ID_table = table_merge[table_merge.ID==i]
    temp_detail['VID'] = i
    temp_detail['realtimeTag'] = []

    for j in range(len(unique_ID_table)):
        query_update = {}
        query_temp = tag_db_query(unique_ID_table['UTID'].values[j],cur)

        query_update['scenario'] = query_temp['scenario'] #將batchTag所需的欄位進行整理
        query_update['recommendWeight'] = query_temp['recommedWeight']
        query_update['dataSource'] = query_temp['dataSource']
        query_update['securityFilter'] = query_temp['securityFilter']
        query_update['tagValue'] = unique_ID_table['TAG_VALUE'].values[j]
        query_update['tagId'] = query_temp['TAG_ID']
        query_update['tagName'] = query_temp['Chinese_Desc'].split('/')
        query_update['tagTime'] = time.time()
        query_update['expireTime'] = time.time() + float(query_temp['expireAfter'])
        query_update['isValid'] = query_temp['isActive']
        temp_list.append(query_update)

    temp_detail['batchTag'] = temp_list
    r0.set(i, json.dumps(temp_detail,ensure_ascii=False)) #將VID,batchTag和realtimeTag等資料透過redis DB來存取

unique_tagValue = list(np.unique(table2['TAG_VALUE']))
for value in unique_tagValue:
    offer_list = {"tag_value":value, "offer_list":offer_db_query(value, cur)['offer_list']}
    r1.set(value, offer_list) #將offer_list透過redis DB來存取
