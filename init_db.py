# 필요한 모듈(pymongo, requests, jsonify, json) import
import requests, json, datetime, telegram
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# pymongo db 만들기
client = MongoClient('localhost', 27017)
db = client.dbopca

########################################### API 만들기 ###########################################
## 오피넷 유가정보 무료 API 파싱 ##
####### << 오피넷 오픈 API 이용 정보 >> #######
## 1. 지역코드 얻기 #######
# url = http://www.opinet.co.kr/api/areaCode.do?out=json&code=${APIkey}
## 2. 주유소 좌표정보 얻기 #######
# url = http://www.opinet.co.kr/api/searchByName.do?code=${APIkey}&out=json&osnm=${상호명}&area=${지역코드}

## 3. 경쟁주유소들 고유ID 얻기 #######
# url = http://www.opinet.co.kr/api/aroundAll.do?code=${APIkey}&x=${X좌표}&y=${Y좌표}&radius=${반경}&sort=1&prodcd=${상품코드}&out=json

## 4. 주유소 상세정보 얻기 #######
# url = http://www.opinet.co.kr/api/detailById.do?code=${APIkey}&id=${주유소ID}&out=json


# 고정값 #
apiKey = '무료API키'  # API key
areaName = '경기'  # 지역이름
myOilBankName = '분당탑주유소'  # 주유소상호명
prodcd = {  # 상품코드
    "gasolin": 'B027',
    "disel": 'D047',
    "kerosene": 'C004'
}
radius = 3000  # 반경(단위:미터)


## 지역코드 얻는 함수
# input  : API key
# output : 지역코드
def getAreaCode(apiKey):
    url = f'http://www.opinet.co.kr/api/areaCode.do?out=json&code={apiKey}'
    data = requests.get(url)
    apiStrToJson = json.loads(data.text)
    codes = apiStrToJson["RESULT"]["OIL"]
    for item in codes:
        if item["AREA_NM"] == areaName:
            areaCode = item["AREA_CD"]
    return areaCode


## 주유소 x,y 좌표 얻는 함수
# input  : API key, 주유소상호명, 지역코드
# output : 주유소좌표정보
def getCoordinate(apiKey, oilBankName, areaCode):
    url = f'http://www.opinet.co.kr/api/searchByName.do?code={apiKey}&out=json&osnm={myOilBankName}&area={areaCode}'
    data = requests.get(url)
    apiStrToJson = json.loads(data.text)
    coordinate = {
        'x': apiStrToJson["RESULT"]["OIL"][0]["GIS_X_COOR"],
        'y': apiStrToJson["RESULT"]["OIL"][0]["GIS_Y_COOR"],
    }
    return coordinate


## 반경 내 경쟁주유소 고유 ID 얻는 함수
# input  : API key, 주유소좌표정보, 반경(단위:미터), 상품코드
# output : 경쟁주유소ID들(리스트)
def getCompetitionOilbankID(apiKey, coordinate, radius, prodcd):
    url = f'http://www.opinet.co.kr/api/aroundAll.do?code={apiKey}&x={coordinate["x"]}&y={coordinate["y"]}&radius={radius}&sort=1&prodcd={prodcd["gasolin"]}&out=json'
    data = requests.get(url)
    apiStrToJson = json.loads(data.text)
    competitionOilbankIDs = []
    competitonOilbankList = apiStrToJson["RESULT"]["OIL"]
    for item in competitonOilbankList:
        competitionOilbankIDs.append(item["UNI_ID"])
    return competitionOilbankIDs


## 경쟁주유소들의 상세정보 얻는 함수
# input  : API key, 주유소ID
# output : 경쟁주유소상세정보(딕셔너리)
def getCompetitionOilbankInfo(apiKey, oilbankID):
    url = f'http://www.opinet.co.kr/api/detailById.do?code={apiKey}&id={oilbankID}&out=json'
    data = requests.get(url)
    apiStrToJson = json.loads(data.text)
    competitionOilbankInfo = apiStrToJson["RESULT"]["OIL"][0]
    return competitionOilbankInfo


## API 구조를 만드는 함수
def makeAPI(apiKey, oilbankIDs):
    api = {"Result": 'success', "oil": []}
    for item in oilbankIDs:
        api["oil"].append(getCompetitionOilbankInfo(apiKey, item))
    return api


areaCode = getAreaCode(apiKey)
coordinate = getCoordinate(apiKey, myOilBankName, areaCode)
competitionOilbankIDs = getCompetitionOilbankID(apiKey, coordinate, radius, prodcd)
api = makeAPI(apiKey, competitionOilbankIDs)


###########################################################################################################
########################################### OPCA DB 만들기 ###########################################
### 초기화 DB 만들기 ###
def initalizeDB(api):
    oilbankLists = api["oil"]
    date = datetime.datetime.now()
    init_db = []
    # API에서 불러온 데이터를 DB에 넣기위해 for문이용
    for item in oilbankLists:
        initial_db = {
            "oilbank_name": "",
            "oilbank_brand": "",
            "gasoline_price": {
                "before": {"price": 0, "date": ""},
                "current": {"price": 0, "date": ""},
                "changed": {"check": False, "value": 0}
            },
            "disel_price": {
                "before": {"price": 0, "date": ""},
                "current": {"price": 0, "date": ""},
                "changed": {"check": False, "value": 0}
            },
            "checked": False
        }
        initial_db["oilbank_name"] = item["OS_NM"]
        initial_db["oilbank_brand"] = item["POLL_DIV_CO"]
        initial_db["gasoline_price"]["current"]["date"] = date
        initial_db["disel_price"]["current"]["date"] = date
        for price in item["OIL_PRICE"]:
            if price["PRODCD"] == "B027":
                gasoline_price = {"before": {"price": 0, "date": ""},
                                  "current": {"price": price["PRICE"], "date": date},
                                  "changed": {"check": False, "value": 0}}
                initial_db["gasoline_price"] = gasoline_price
            elif price["PRODCD"] == "D047":
                disel_price = {"before": {"price": 0, "date": ""},
                               "current": {"price": price["PRICE"], "date": date},
                                "changed": {"check": False, "value": 0}}
                initial_db["disel_price"] = disel_price
        init_db.append(initial_db)
    return init_db

db.opca_db.insert_many(initalizeDB(api))