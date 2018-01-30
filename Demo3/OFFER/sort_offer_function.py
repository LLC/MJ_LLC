import pandas as pd
import redis
import json
import math

ip = 'redis'
r0 = redis.Redis(host=ip, port=6379, db=0)

xls = pd.ExcelFile('OfferTag_1120.xlsx')
offer_label_table = xls.parse('OFFER ID') #讀取excel中OFFER ID這個資料表

offer_label_tag = list(offer_label_table)[3:-1] #取得欄位名稱LABEL1~LABEL18(最後一個LABEL)
offer_label_tag

# All tags of each offer id
offer_label_table['offer_label_list'] = ""
offer_label_Json = []

for i in range(offer_label_table.shape[0]): 
    temp_list = []
    temp_detail = {}
    temp_detail['offer_id'] = str(offer_label_table.loc[i,:]['OFFER_ID']) #將每一個OFFER ID存到temp_detail這個dictionary之中
    
    for column in offer_label_tag:
        if not pd.isnull(offer_label_table.loc[i,:][column]): #將每一個OFFER的所有LABEL都存入temp_list之中
            temp_list.append(offer_label_table.loc[i,:][column])
        else:
            break
            
    offer_label_table.loc[i,:]['offer_label_list'] = temp_list
    temp_detail['label'] = temp_list
    offer_label_Json.append(temp_detail)

def clean_data(lst):
	new_lst = []
	# Delete u before offer_id
	for i in range(len(lst)):
		new_lst.append(str(lst[i]))  
	return new_lst

def get_recommend_offer(vid, tagid, lst):
	offer_score = []
	recommend_offer =[]
	for off in lst:
	    for j in range(len(offer_label_Json)):
	        if off == offer_label_Json[j]['offer_id']:
	            offer_score.append(get_tag_cos(usr_tags(vid, tagid), offer_label_Json[j]['label']))

	while(len(recommend_offer) < len(offer_score)):
	    recommend_offer.append(lst[offer_score.index(max(offer_score))])
	    offer_score[offer_score.index(max(offer_score))] = -1
	  
	return recommend_offer

# All tags of one vid
def usr_tags(vid, tagid):
	usr_tags = []
	for i in range(len(json.loads(r0.get(vid))['batchTag'])):
	    if str(json.loads(r0.get(vid))['batchTag'][i]['tagId']) == tagid:
	        for j in range(len(json.loads(r0.get(vid))['batchTag'][i]['tagName'])):
	            usr_tags.append(json.loads(r0.get(vid))['batchTag'][i]['tagName'][j])

	return usr_tags

def get_tag_cos(TL1,TL2): #Cosine Similarity Algorithm
    return (len([t for t in TL1 if t in TL2])/math.sqrt(len(TL1)*len(TL2)))
