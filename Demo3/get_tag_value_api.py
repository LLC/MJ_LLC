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
import requests
import psycopg2

ip = 'redis'
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
r0 = redis.Redis(host=ip, port=6379, db=0)

'''
# connect PostgreSQL
conn = psycopg2.connect(database = "MJ",
                        host = "localhost",
                        user = "llc",
                        password = "")
cur = conn.cursor()

def offer_db_query(TAG_VALUE, sql_db):
    SQL = "SELECT tag_info FROM offer_db WHERE tag_info->>'Tag_value' = '{}';".format(TAG_VALUE)
    sql_db.execute(SQL)
    records = sql_db.fetchall()[0][0]
    return records
'''

@app.route('/GetTag',methods=['GET']) #名為GetTag的API是採用GET的方法
def get_tag():
    print 'Hi'
    vid = request.args.get('vid') #需要輸入VID,tagID
    tagid = request.args.get('tagid')
    tag_info = json.loads(r0.get(vid))

    for k in range(len(tag_info.values()[0])):
    	if str(tag_info.values()[0][k]['tagId']) == str(tagid):
    		tag_info_detail = tag_info.values()[0][k] 
    		break
    
    res = jsonify(tag_info_detail)
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    return res

@app.route('/GetTagValue',methods=['GET']) #名為GetTagValue的API是採用GET的方法
def get_tagValue():
    print 'Hi'
    vid = request.args.get('vid') #需要輸入VID,tagID
    tagid = request.args.get('tagid')
    tag_info = json.loads(r0.get(vid))

    for k in range(len(tag_info.values()[0])):
    	if str(tag_info.values()[0][k]['tagId']) == str(tagid):
    		tag_info_detail = tag_info.values()[0][k]['tagValue'] 
    		break
    
    res = jsonify(tag_info_detail) 
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    return res #會回傳顧客所屬客群

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80) #6004
