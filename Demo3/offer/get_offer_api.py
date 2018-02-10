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
tagging = 'llc_get_tag_value_api'
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
r1 = redis.Redis(host=ip, port=6379, db=1)


@app.route('/GetOfferList',methods=['GET']) #API名稱為GetOfferList，運用Get的方式
def get_offerlist():
	vid = str(request.args.get('vid')) #需要取得虛擬ID和TagID兩個變數
	tagid = str(request.args.get('tagid')) 
	url = "http://%s/GetTagValue"%tagging #呼叫另一支GetTagValue的API
	data = {'vid':vid, 'tagid':tagid}
	tag_info = requests.get(url, params=data)	
	tag_value = int(tag_info.content) #取到客群值的格式為str，將其轉為int
	offer_list = r1.get(tag_value) #呼叫redis DB並取得推薦內容
	
	tmp = offer_list.replace("'",'"') #offer_list資料格式轉換
	test = re.sub(ur'u"','"',tmp)
	offer_dict = json.loads(test) #將其轉為json格式
	offer_list = offer_dict['offer_list'] #並取得offer_list這個key所對應的value
	
	# Sort offer according to offer score 

	recommend_offer_list = sort_offer_function.get_recommend_offer(vid, tagid, offer_list) #將推薦內容透過演算法進行排序
	recommend_dict = {'offer_list':recommend_offer_list}
	sorted_offer_list = jsonify(recommend_dict)

	return sorted_offer_list

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80) #6003
