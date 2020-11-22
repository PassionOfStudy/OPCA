## 업데이트 되기 전 DB 데이터 저장

# 필요한 모듈(pymongo, requests, jsonify, json) import
import requests, json, datetime, telegram
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# pymongo db 만들기
client = MongoClient('localhost', 27017)
db = client.dbopca

#Telegram Bot Message Sender 사용시 필요한 데이터
TELEGRAM_TOKEN = '텔레그램 토큰값'
bot = telegram.Bot( token=TELEGRAM_TOKEN )
updates = bot.getUpdates()
chat_id = updates[-1].message.chat.id

# Telegram Push Message Sender
def pushTelegramMessage(oilbank_name, gasoline, disel):
    if gasoline["changed"]["value"] < 0:
        bot.sendMessage(chat_id=chat_id,
                        text=f'{oilbank_name}가 \n휘발유가격을 {abs(gasoline["changed"]["value"])}원 올렸습니다.'.format(chat_id))
    else :
        bot.sendMessage(chat_id=chat_id,
                        text=f'{oilbank_name}가 \n휘발유가격을 {abs(gasoline["changed"]["value"])}원 내렸습니다.'.format(chat_id))
    if disel["changed"]["value"] < 0:
        bot.sendMessage(chat_id=chat_id,
                        text=f'{oilbank_name}가 \n경유가격을 {abs(disel["changed"]["value"])}원 올렸습니다.'.format(chat_id))
    else:
        bot.sendMessage(chat_id=chat_id,
                        text=f'{oilbank_name}가 \n경유가격을 {abs(disel["changed"]["value"])}원 내렸습니다.' .format(chat_id))
    # bot.sendMessage(chat_id=chat_id, text=f'{oilbank_name}의 \n휘발유가격이 {gasolineDiffValue}, \n경유가격이 {diselDiffValue} \n 변동되었습니다..'.format(chat_id))
    bot.sendMessage(chat_id=chat_id,
                    text=f'현재 {oilbank_name}의 \n휘발유가격 : {gasoline["current"]["price"]}, \n경유가격 : {disel["current"]["price"]} \n입니다. '.format(chat_id))
    return 0

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
apiKey = 'Open API Key'  # API key
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
### DB에 조회한 데이터 업데이트하기 ###
#: current -> before, 조회한 데이터 -> current
def updateDB():
    opca_db = list(db.opca_db.find({}, {'_id': 0}))
    date = datetime.datetime.now()
    for opcaDB, opcaAPI in zip(opca_db, api["oil"]):
        gasoline_price = {}
        disel_price = {}
        before_gasoline_price = {
            "price": opcaDB["gasoline_price"]["current"]["price"],
            "date": opcaDB["gasoline_price"]["current"]["date"]}
        before_disel_price = {
            "price": opcaDB["disel_price"]["current"]["price"],
            "date": opcaDB["disel_price"]["current"]["date"]}
        for price in opcaAPI["OIL_PRICE"]:
            if price["PRODCD"] == "B027":
                current_gasoline_price = {"price": price["PRICE"], "date": date}
                gasoline_only_price = {"before": before_gasoline_price, "current": current_gasoline_price}
                gasoline_price = {
                    "before": gasoline_only_price["before"],
                    "current": gasoline_only_price["current"],
                    "changed": changedGasolinePrice(gasoline_only_price)}
            elif price["PRODCD"] == "D047":
                current_disel_price = {"price": price["PRICE"], "date": date}
                disel_only_price = {"before": before_disel_price, "current": current_disel_price}
                disel_price = {
                    "before": disel_only_price["before"],
                    "current": disel_only_price["current"],
                    "changed": changedDiselPrice(disel_only_price)}
        ## mongoDB 업데이트
        db.opca_db.update_many({"oilbank_name": opcaAPI["OS_NM"]},
                          {'$set': {
                              "gasoline_price": gasoline_price,
                              "disel_price": disel_price,
                              "checked": checkedWholeChange(gasoline_price, disel_price)}})
        ## 가격변동시 텔레그램 푸쉬알람 발생
        if checkedWholeChange(gasoline_price, disel_price):
            # pushTelegramMessage(opcaAPI["OS_NM"], gasoline_price["changed"]["value"], disel_price["changed"]["value"])
            pushTelegramMessage(opcaAPI["OS_NM"], gasoline_price, disel_price)
    return 0

def changedGasolinePrice(gasolinePrice):
    gasoline_price_changed = {}
    if gasolinePrice["before"]["price"] != gasolinePrice["current"]["price"]:
        gasoline_price_changed = {"check": True, "value": gasolinePrice["before"]["price"] - gasolinePrice["current"]["price"]}
    else:
        gasoline_price_changed = {"check": False, "value": 0}
    return gasoline_price_changed

def changedDiselPrice(diselPrice):
    disel_price_changed = {}
    if diselPrice["before"]["price"] != diselPrice["current"]["price"]:
        disel_price_changed = {"check": True, "value": diselPrice["before"]["price"] - diselPrice["current"]["price"]}
    else:
        disel_price_changed = {"check": False, "value": 0}
    return disel_price_changed

def checkedWholeChange(gasoline, disel):
    if gasoline["changed"]["check"] or disel["changed"]["check"]:
        result = True
    else:
        result = False
    return result


updateDB()