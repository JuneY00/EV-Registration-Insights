from flask import Flask, jsonify, request
from blueprints.api import fetch_data
from dotenv import load_dotenv
import os 
from flask import Flask, render_template

load_dotenv()

API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# API를 호출하고 데이터를 반환하는 라우트
@app.route('/api/get_data', methods=['GET'])
def get_data():
    # 요청 시 필요한 파라미터 설정
    params = {
        'serviceKey': API_KEY,
        'pageNo': request.args.get('pageNo', '1'),  # 기본값으로 '1' 설정
        'numOfRows': '10',  # 한 페이지에 표시할 항목 수 (예: 10)
        'type': 'json',     # 응답 데이터 형식 (예: JSON)
        # 필요한 다른 파라미터 추가
    }

    # API로부터 데이터 가져오기
    data = fetch_data(params)
    
    # Flask에서 JSON으로 반환
    return jsonify(data)

# Flask 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
