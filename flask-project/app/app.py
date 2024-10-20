from flask import Flask, jsonify, request, Response, render_template
from blueprints.api import fetch_car_cnt  # fetch_car_cnt만 가져옴
from dotenv import load_dotenv
import os 
import json
import requests  # 외부 API 호출을 위해 추가
from functools import lru_cache

# 환경 변수 로드 
load_dotenv()

# fetch_data 함수 정의
def fetch_data(endpoint, api_key, params):
    try:
        params['apiKey'] = api_key
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        return response.json()  # JSON 형식으로 데이터 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

class DataLoader:
    @staticmethod
    def load_json_data(filename):
        file_path = os.path.join(os.path.dirname(__file__), filename)  
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
class EVChargeService:
    def __init__(self):
        self.ENDPOINT_EVcharge = 'https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do'
        self.API_KEY_EVcharge = os.getenv('API_KEY_EVcharge')         

    @lru_cache(maxsize=128)
    def get_ev_info(self, sido_code):
        params = {
            'apiKey': self.API_KEY_EVcharge,
            'metroCd': sido_code,  # ex. 지역 코드 
            'returnType':'json'
        }

        data = fetch_data(self.ENDPOINT_EVcharge, self.API_KEY_EVcharge, params)
    
        # place name, carType, stnPlace 
        EVcharge_data = []
        for item in data.get('data', []):
            EVcharge_data.append({
                'metro': item['metro'],
                'city': item['city'],
                'stnPlace': item['stnPlace'],
                'stnAddr': item['stnAddr'], 
                'rapidCnt': item['rapidCnt'],
                'slowCnt': item['slowCnt'],
                'carType': item['carType']
            })

        return EVcharge_data

    def get_ev_data(self):
        data = DataLoader.load_json_data('SidoCode.json')
        results = []
        
        for item in data:
            sido_code = item['code']
            ev_data = self.get_ev_info(sido_code)
            results.append((item['region'], ev_data))
        
        return results


class EVChargeApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.ev_service = EVChargeService()
        self.configure_routes()
        
    def configure_routes(self):
        @self.app.route('/api/get_EVinfo/all')
        def get_EVInfo_All():
            return jsonify(self.get_ev_info_all())
        
        @self.app.route('/api/get_EVinfo/CType')
        def get_EVInfo_ChargerType():
            return jsonify(self.get_ev_info_charger_type())
        
        @self.app.route('/EVcharge/barChart')
        def EVcharge_barChart():
            return render_template('EVCharger_barChart.html')

        @self.app.route('/EVcharge/lists')
        def EVcharge_table():
            return render_template('EVCharger_lists.html')
        
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/index')
        def index():
            return render_template('index.html')

    def get_ev_info_all(self):
        results = []
        ev_data = self.ev_service.get_ev_data()

        for _, data in ev_data:
            results.append(data)

        return results

    def get_ev_info_charger_type(self):
        results = {}
        ev_data = self.ev_service.get_ev_data()
        
        for region, data in ev_data:
            rapid_total = sum(d['rapidCnt'] for d in data)
            slow_total = sum(d['slowCnt'] for d in data)

            results[region] = {
                'rapidTotal': rapid_total,
                'slowTotal': slow_total
            }
        
        return results
    
    def run(self):
        self.app.run(debug=True)


# 기존의 carCnt API를 위한 Flask 앱 정의
app = Flask(__name__)

# API를 호출하고 데이터를 반환하는 라우트
@app.route('/api/carCnt', methods=['GET'])
def get_carCnt():
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
    use_ev_charge_app = False  # True로 설정하면 EVChargeApp을 실행, False면 app.run() 실행
    
    if use_ev_charge_app:
        ev_charge_app = EVChargeApp()
        ev_charge_app.run()
    else:
        app.run(host='127.0.0.1', port=5001, debug=True)
