## 업데이트 되기 전 DB 데이터 저장

# 필요한 모듈 import(pymongo)
from pymongo import MongoClient
import api

# pymongo db 만들기
client = MongoClient('localhost', 27017)
db = client.dbopca

# collection 생성 및 데이터 DB에 저장
initial_db = db.oilbanks_info.insert(api.api['oil'])