import sys
from flask import Flask
from flask import request
import tag_function
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello():
    return "HI! This is Tagging System"

@app.route('/AddRealtimeTag',methods=['POST'])
def AddRealtimeTag():
    print("Add realtimeTag")
    vid = request.args.get('vid')
    tagid = request.args.get('tagid')
    print('vid = '+vid+'; tagid = '+utid)
    add_realtimeTag_function.add_realtime_tag(vid, tagid)
    res = jsonify({"status":"tagging"})
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'        
    return res

"""
@app.route('/getAllBehaviorTags',methods=['GET'])
def getAllBehaviorTags():
    print("Get All Behavior Tags")
    vid = request.args.get('vid')
    res = jsonify(tag_function.get_behavior(vid))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'    
    return res
"""

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=6005)
