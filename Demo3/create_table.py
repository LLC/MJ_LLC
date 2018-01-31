# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime
import time
import json
import psycopg2
import redis
import sys

reload(sys)
sys.setdefaultencoding('utf8') 

#將意圖標籤資料表進行前處理，並轉為JSON格式存入ProsgreSQL DB
intent_table = pd.read_excel("INTENT_TAG.xlsx")
intent_tag = list(intent_table)

intent_table['intent_list']=''
intent_Json = []
for i in range(intent_table.shape[0]):
    temp_detail = {}
    for column in intent_tag:
        temp_detail[column]=str(intent_table.loc[i,:][column])
    
    scenario = intent_table.scenario[i].split('|')

    temp_detail['scenario'] = {'DIIS1' : '',
                               'DIIS2' : '',
                               'DIIS3' : ''}
    
    for j in range(len(scenario)):
        DIIS = 'DIIS' + str(j+1)
        temp_detail['scenario'][DIIS] = scenario[j]
    
    intent_Json.append(temp_detail)

database='postgres'
host = 'postgres'
user = 'postgres'
password = ''

conn = psycopg2.connect(database = database,
                        host = host,
                        user = user,
                        password = password)
cur = conn.cursor()

cur.execute("select * from information_schema.tables where table_name='intent_db';")
if bool(cur.rowcount):
    print 'intent_db is exist!'
    pass

else:
    SQL = "CREATE TABLE intent_db(id serial PRIMARY KEY,tag_info json NOT NULL);"
    cur.execute(SQL)
    conn.commit()
    print "Create Table Done!"

for i in intent_Json:
    SQL = "INSERT INTO intent_db(tag_info) VALUES('{}' );".format(json.dumps(i))
    cur.execute(SQL)
    conn.commit()


#將各個客群適合推薦的offer進行前處理，並轉為JSON格式存入ProsgreSQL DB
xls = pd.ExcelFile('OfferID_LIST_TAG.xlsx')
offer_table = xls.parse('Data_Offer')

offer_tag = list(offer_table)[2:]

offer_table['offer_list'] = ""
offer_Json = []
for i in range(offer_table.shape[0]):
    temp_list = []
    temp_detail = {}
    temp_detail['tag_value'] = str(offer_table.loc[i,:]['UTID'])
    
    for column in offer_tag:
        temp_list.append(offer_table.loc[i,:][column])
    offer_table.loc[i,:]['offer_list'] = temp_list
    temp_detail['offer_list'] = temp_list
    offer_Json.append(temp_detail)

cur.execute("select * from information_schema.tables where table_name='offer_db';")
if bool(cur.rowcount):
    print 'offer_db is exist!'
    pass

else:
    SQL = "CREATE TABLE offer_db(id serial PRIMARY KEY,tag_info json NOT NULL);"
    cur.execute(SQL)
    conn.commit()
    print "Create Table Done!"

for i in offer_Json:
    SQL = "INSERT INTO offer_db(tag_info) VALUES('{}');".format(json.dumps(i))
    cur.execute(SQL)
    conn.commit()
