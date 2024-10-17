from flask import Flask, jsonify, request, Response
from blueprints.api import fetch_data, fetch_car_cnt
from dotenv import load_dotenv
import os 
import json
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



# API를 호출하고 데이터를 반환하는 라우트
@app.route('/api/carCnt', methods=['GET'])
def get_carCnt():
    # 요청 시 필요한 파라미터 설정
    try:
      year = request.args.get('year')
      region = request.args.get('do')

      # API로부터 데이터 가져오기
      data = fetch_car_cnt(year, region)

      # Flask에서 JSON으로 반환
      return Response(
          json.dumps(data, ensure_ascii=False),
          content_type='application/json; charset=utf-8'
      )
    except Exception as e:
        return render_template('500.html'), 500

# Flask 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
