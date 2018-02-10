# MJ_LLC(POC)

## 客群推薦系統

### Structure
```python
├─Demo3
│     ├──
│      OFFER 
│         ├── Dockerfile              #dockerfile   
|         ├── OfferTag_1120.xlsx      #offerTag
|         ├── get_offer_api.py        #input tagValue and output recommended offer_list
|         └── sort_offer_function.py  #sort offer_list according to tag similarity between customer and offer
│     │     
│     ├── .DS_Store
│     ├── Dockerfile                  #dockerfile
│     ├── INTENT_TAG.xlsx             #intent tag metadata
│     ├── OfferID_LIST_TAG.xlsx       #different TA Get different offer_list
│     ├── TAG_LOG_DOWNLOAD.xlsx       #comparison table(ID/UTID)
│     ├── TAG_Value_DOWNLOAD.xlsx     #comparison table(ID/UTID/TagValue)
│     ├── api_assist.py               #content raw metadata to redis
│     ├── create_table.py             #read spreadsheet, turn to JSON type and store in PostgreSQL DB
│     ├── get_tag_value_api.py        #input VID and output tag_info or tagValue
│     └── requirements.txt            #docker requirements
│
├─.DS_Store
├─README.md
└─docker-compose.yml             #docker-compose file
```

## Usage
### Demo3 
use docker to build images & container.
``` 
$ docker-compose up
```
