#-*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json
import psycopg2


# connect PostgreSQL
conn = psycopg2.connect(database = "MJ_PROTOTYPE",
                        host = "localhost",
                        user = "chienan",
                        password = "")
cur = conn.cursor()

# Read Data
Intent = pd.read_excel('INTENT_TAG.xlsx')

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
TagDB = TagDb_ETL(Intent)

# Insert Data into PostgreSQL
for i in TagDB:
    SQL = "INSERT INTO tag_db(tag_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    conn.commit()

print 'Tag DB ETL Done!'
