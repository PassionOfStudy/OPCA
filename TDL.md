# To Do List

## 프로젝트 (기간 : 11/01 ~ 11/14)
###➤ _프로젝트 시작 전_

####_프로젝트 기획_
* 프로젝트 소개 
-[ ] _README.md_ 만들기

####_프로젝트 개발환경 설치_
* **Pycharm(IDE) 환경 설정**
  * Python 패키지 설치 및 설정
   -[X] **flask** - Flask Server
   -[X] **pymongo** - MongoDB
* **버전 컨트롤 시스템(github) 설정**
  * Github Repository 생성
   -[X] **my_project**

###➤ _프로젝트 시작_

####◎ _Front End_
* **메인 홈페이지 전체 HTML 작성**
  * **전체 레이아웃 작성**
   -[X] **Header** - 로고, 네비게이션
   -[X] **Section(main)** - 소개, 테이블
   -[ ] **Footer** - 미정
  * **JavaScript 작성**
   -[X] 페이지 로드 시 초기화
   -[X] 버튼 클릭시 API를 조회하여 데이터를 표형식으로 파싱   
  * **HTML, CSS, JavaScript 분리하기**
   -[X] **HTML** - index.html
   -[X] **CSS** - style.css
   -[ ] **JavaScript** - script.js

####◎ _Back End_
* **Flask Server 코드 작성 - _app.py_**
  * _"app.py"_
   -[X] 필요한 모듈들 import
   -[X] Flask Web Server 구동
   -[X] API 불러와서 Client에 전달하는 코드 작성 
* **나만의 API 코드 작성 - _"api.py"_**
  * _api.py_
   -[X] 반경 내 주유소 경쟁 주유소 정보 가져오기
* **MongoDB 저장 코드 작성 - _"db.py"_**
  * _db.py_
   -[X] 나만의 API를 읽어와서 저장하는 코드 작성
   -[X] DB에 저장된 데이터를 읽어오는 코드 작성
   -[ ] 과거 DB데이터와 현재 조회 데이터 비교 코드 작성
   -[ ] 과거 DB에 저장된 데이터와 현재 조회한 데이터 비교 코드 작성
* **자동 스크립트 작성 - _autoAlarm.sh_**
  * _autoAlarm.sh_
   -[ ] 1시간마다 db.py를 실행하는 코드 작성
   -[ ] 업데이트된 정보가 있다면 Telegram 메신저 자동 푸쉬 알림
* **텔레그램 Open API를 이용한 푸쉬알림 코드 작성 - autoAlarm.py**
  * _autoAlarm.py_
  -[ ] 자동 bot father 생성 
  -[ ] AWS Server에서 호출하면 푸쉬알림을 주는 코드 작성