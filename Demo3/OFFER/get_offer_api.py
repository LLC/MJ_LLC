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
import re
import sort_offer_function

ip = 'redis'
#tagging = 'tagserver'
tagging = 'llc_get_tag_value_api'
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
r1 = redis.Redis(host=ip, port=6379, db=1)

@app.route('/GetOfferList',methods=['GET'])
def get_offerlist():
	vid = str(request.args.get('vid'))
	tagid = str(request.args.get('tagid'))
	url = "http://%s/GetTagValue"%tagging
	data = {'vid':vid, 'tagid':tagid}
	tag_info = requests.get(url, params=data)	
	#tag_info = json.loads(tag_info.content)
	tag_value = int(tag_info.content)
	#print r.get(tag_info.conent)
	offer_list = r1.get(tag_value)
	
	tmp = offer_list.replace("'",'"')
	test = re.sub(ur'u"','"',tmp)
	offer_dict = json.loads(test)
	offer_list = offer_dict['offer_list']
	#offer_list = jsonify(offer_list)
	#return offer_list
	
	# Sort offer according to offer score 

	recommend_offer_list = sort_offer_function.get_recommend_offer(vid, tagid, offer_list)
	recommend_dict = {'offer_list':recommend_offer_list}
	sorted_offer_list = jsonify(recommend_dict)

	return sorted_offer_list

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80) #6003
