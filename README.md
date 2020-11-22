<img src="https://user-images.githubusercontent.com/17819874/79853717-5db2f900-8403-11ea-99ba-ed0bb3cdb9ef.png" height="100"/>

# OPCA(오피카, Oilbank Price Change Alarm)  
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/ohahohah/readme-template/graphs/commit-activity) 
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)



> 주유소 가격 변동 알리미 
- 반경 3km이내의 경쟁 주유소들의 가격이 변경되면 자동으로 알림을 주는 자동봇

## 핵심 기능  Key Feature
- 초기 오피넷에서 제공하는 Open API에서 반경 3km내의 경쟁 주유소 가격을 불러와 DB에 저장한다.
- 이 후 매 시간마다 경쟁 주유소 정보들을 조회하고 이전 DB자료와 비교하여 가격이 변동되면 메신저로 자동 알림.
 
## 사용 How To Use
- 설치환경
  - Use Tools
    - PyCharm 2020.2.3 (Professional Edition)
    - Robo 3T 1.4.1 (Build 122dbd9)
    - FileZill 3.51.0
    
  - Programming Language
    - python 3.8
    - packages : pymongo, python-telegram-bot, requests
    
 - Use Server
   - RaspberryPi3(Raspbian OS)

- 실행준비 및 실행
  - installpip3.sh, isntallmongodb.sh 실행
  - init_db.py와 opca_db.py 서버에 업로드
  - init_db.py 실행 전
    - init_db.py 파일 값 변경
      - ```client = MongoClient('mongodb://아이디:비밀번호@localhost', 27017)```
      - ```apiKey = 무료API키 넣기```
  - init_db.py 실행
    - ```python init_db.py```
  - init_db.py 실행 후
    - opca_db.py 파일 값 변경
      - ``````client = MongoClient('mongodb://아이디:비밀번호@localhost', 27017)``````
      - ```apiKey = 무료API키 넣기```
      - ```TELEGRAM_TOKEN = '텔레그램 토큰값'```
    - opca_sh 작성
      - ```#!/bin/bash ```
      - ```python /절대경로/opca_db.py ```
    - 서버 clonetab 등록
      - ```0 */1 * * * . /home/ubuntu/opca/opca.sh >> /home/ubuntu/opca/log/temp.log```
      - 정상적으로 작동되는지 log/temp.log 파일에 시간기록
      - 정상적으로 작동되는지 log/temp에 시간


## Reference
- [오피넷 유가정보 Free Open API](http://www.opinet.co.kr/user/custapi/custApiInfo.do) : 반경 내 경쟁주유소 정보 활용 

## Links
- Repository: https://github.com/PassionOfStudy/my_project