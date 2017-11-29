#-*- coding:utf-8 -*-
import os
import sys
import json
import operator
from flask import Flask,g
import time
import pandas as pd
from flask import jsonify
import json
import inspect
import redis
from flask import request

redis_ip = 'localhost'
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = redis.Redis(host=redis_ip,port=6379,db=0)

@app.route('/GetAllTag',methods=['GET'])
def get_alltag():
    vid = request.args.get('vid')
    tag_info = json.loads(conn.get(vid))
    res = jsonify(tag_info)
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    return res


@app.route('/GetAllInterest',methods=['GET'])
def get_interesttag():
    vid = request.args.get('vid')
    tag_info = json.loads(conn.get(vid))
    res = query_DIIS(tag_info, 'H')
    if type(res) <> str:
        res = jsonify(res)
        res.headers['Content-Type'] = 'application/json; charset=utf-8'
        return res
    return "Can't find it in DB"

@app.route('/GetAllIntention',methods=['GET'])
def get_intentiontag():
    vid = request.args.get('vid')
    tag_info = json.loads(conn.get(vid))
    res = query_DIIS(tag_info, 'I')
    if type(res) <> str:
        res = jsonify(res)
        res.headers['Content-Type'] = 'application/json; charset=utf-8'
        return res
    return "Can't find it in DB"

# 查詢Tag為Intension或Interest

def query_DIIS(tag, scenario):
    query = []
    for i in tag['batchTag']:
        if (str(i['scenario']['DIIS1']) == scenario):
            query.append(i)
    tag['batchTag'] = query
    if len(tag['batchTag']) == 0:
        return "No interest"
    return tag


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6004)
