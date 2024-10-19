# model/ev_charge_service.py
import os
from functools import lru_cache
from dotenv import load_dotenv
import requests

class EVChargeModel:
    def __init__(self):
        # .env 파일에서 환경 변수 로드
        load_dotenv()
        self.ENDPOINT_EVcharge = 'https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do'
        self.API_KEY_EVcharge = os.getenv('API_KEY_EVcharge')         


    @lru_cache(maxsize=128)
    def fetch_ev_charge_data(self, sido_code):
        params = {
            'apiKey': self.API_KEY_EVcharge,
            'metroCd': sido_code,  # ex. 지역 코드 
            'returnType':'json'
        }     
        
        data = self.fetch_data(self.ENDPOINT_EVcharge, self.API_KEY_EVcharge, params)
        
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


   # 데이터 가져오기 함수
    def fetch_data(self,endpoint, api_key, params):
        try:
            params['apiKey'] = api_key
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
            return response.json()  # JSON 형식으로 데이터 반환
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

