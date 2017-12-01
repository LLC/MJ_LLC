import json
import redis
import requests
from pymongo import MongoClient
import psycopg2
from flask import jsonify
import time
import re

ip = 'localhost'

r0 = redis.Redis(host=ip, port=6379, db=0)

conn = psycopg2.connect(database = "MJ",
                        host = "localhost",
                        user = "llc",
                        password = "")
cur = conn.cursor()

def tagging_db_query(tagid, sql_db):
    SQL = "SELECT tag_info FROM intent_db WHERE tag_info->>'TAG_ID' = '{}';".format(tagid)
    sql_db.execute(SQL)
    records = sql_db.fetchall()[0][0]
    return records

def meta_to_realtime(tag_meta):
    meta_to_realtime = {}
    meta_to_realtime['scenario'] = tag_meta['scenario']
    meta_to_realtime['recommendWeight'] = tag_meta['recommedWeight']
    meta_to_realtime['dataSource'] = tag_meta['dataSource']
    meta_to_realtime['securityFilter'] = tag_meta['securityFilter']
    meta_to_realtime['tagValue'] = ""
    meta_to_realtime['tagId'] = tag_meta['TAG_ID']
    meta_to_realtime['tagName'] = tag_meta['Chinese_Desc']
    meta_to_realtime['tagTime'] = time.time()
    meta_to_realtime['expireTime'] = time.time() + float(tag_meta['expireAfter'])
    meta_to_realtime['isValid'] = tag_meta['isActive']
    return meta_to_realtime

def add_realtime_tag(vid, tagid):
    tag_meta = tagging_db_query(tagid, cur)

    if not r0.get(vid):
        a = {"VID":vid, "batchTag":[], "realtimeTag":[meta_to_realtime(tag_meta)]}        
        r0.set(vid, json.dumps(a, ensure_ascii=False))
        print "no this vid, vid added"
    else:
        print "have vid"
        quer = r0.get(vid)
        quer = quer.replace("'",'"')
        quer = re.sub(ur'u"','"',quer)
        tag_info = json.loads(quer)
        print "change to json type"

        #if realtimeTag is []
        if tag_info['realtimeTag'] == []: 
            tag_info['realtimeTag'].append(meta_to_realtime(tag_meta))
            r0.set(vid, json.dumps(tag_info, ensure_ascii=False))
            print "no realtimeTag, realtimeTag added"
        else:
            for i in range(len(tag_info['realtimeTag'])):
                if tag_info['realtimeTag'][i]['dataSource'] == meta_to_realtime(tag_meta)['dataSource'] and \
                tag_info['realtimeTag'][i]['recommendWeight'] == meta_to_realtime(tag_meta)['recommendWeight'] and \
                tag_info['realtimeTag'][i]['scenario'] == meta_to_realtime(tag_meta)['scenario'] and \
                tag_info['realtimeTag'][i]['securityFilter'] == meta_to_realtime(tag_meta)['securityFilter'] and \
                tag_info['realtimeTag'][i]['tagId'] == meta_to_realtime(tag_meta)['tagId'] and \
                tag_info['realtimeTag'][i]['tagName'] == meta_to_realtime(tag_meta)['tagName']:
                    print "realtimeTag is the same, time updated"
                    tag_info['realtimeTag'][i]['tagTime'] = time.time()
                    tag_info['realtimeTag'][i]['expireTime'] = time.time() + float(tag_meta['expireAfter'])
                else:
                    print "realtimeTag added"
                    tag_info['realtimeTag'].append(meta_to_realtime(tag_meta))
            r0.set(vid, json.dumps(tag_info, ensure_ascii=False))

#print r0.get(1508)
#add_realtime_tag(1508, "SEG002")
#print r0.get(1508)

"""
def get_behavior(vid): 
    realtime_tags = json.loads(r0.get(1508))['realtimeTag']
    messages = []
    if realtime_tags:
        for i in range(len(realtime_tags)):
            keys = ['DIIS1','DIIS2','DIIS3']
            for key in keys:
                if realtime_tags[i]['scenario'][key] == "S"
                messages.append(realtime_tags[i])
    return messages

print get_behavior(1500)
"""        

"""
def get_behavior(vid):
    temp = r.hget(vid, "realtime")
    messages = []
    if temp:
        temp = temp.replace("\'", "\"")
        realtime_tags = json.loads(temp)
        messages = [] #necessary?
        for realtime_tag in realtime_tags:
            if str(realtime_tag["scenario"]) == "Behavior":
                messages.append(realtime_tag)
    return messages
"""
