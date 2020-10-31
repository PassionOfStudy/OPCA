## 필요한 모듈(Flask, pymongo) import하기
import api
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# Flask 서버 만들기
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# # API 페이지 테스트 코드
# @app.route('/read')
# def showData():
#     return jsonify(api.api)

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)