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

ip = 'localhost'
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
r1 = redis.Redis(host=ip, port=6379, db=1)

@app.route('/GetOfferList',methods=['GET'])
def get_offerlist():
	vid = str(request.args.get('vid'))
	tagid = str(request.args.get('tagid'))
	url = 'http://localhost:6004/GetTagValue'
	data = {'vid':vid, 'tagid':tagid}
	tag_info = requests.get(url, params=data)	
	#tag_info = json.loads(tag_info.content)
	tag_value = int(tag_info.content)
	#print r.get(tag_info.conent)
	li = r1.get(tag_value)
	return li



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6003)