import json
import redis
import requests
from pymongo import MongoClient
import psycopg2
import api_assist
from flask import jsonify
import time

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

def add_realtime_tag(vid, tagid):
    tag_meta = tagging_db_query(tagid, cur)

    if not r0.get(vid):
        a = {"VID":vid, "batchTag":[], "realtimeTag":[tag_meta]}        
        r0.set(vid, a)
        #print "no vid"
    else:
        tag_info = json.loads(r0.get(vid))
        #r0.delete(vid)
        #if realtimeTag is []
        if not tag_info['realtimeTag']: 
            tag_info['realtimeTag'].append(tag_meta)
            r0.set(vid, tag_info)
            print "no realtimeTag"
        else:
            for i in tag_info['realtimeTag']:
                if i == tag_meta:
                    tag_info['tagTime'] = time.time()
                else:
                    tag_info['realtimeTag'].append(tag_meta)
            r0.set(vid, tag_info)
#   print json.loads(r.get(vid))

add_realtime_tag(1499,'SEG001')
#r.connection_pool.disconnect()
print r0.get(1499)
print "/n"
print json.loads(r0.get(1499))



#def get_behavior(vid): 
#    realtime_tags = json.loads(r.get(vid))['realtimeTag']
#    return realtime_tags
    #messages = []
    #if tag_info:
    #    messages = []
    #    for realtime_tag in realtime_tags:
    #        if realtime_tag['scenario'] == 'S': # S is a behavior example
    #            messages.append(realtime_tag)
    #return messages

#print get_behavior(1500)
           
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
