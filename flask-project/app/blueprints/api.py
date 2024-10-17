from flask import Flask, jsonify, request
import requests
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# API 호출에 필요한 정보
ENDPOINT = "http://apis.data.go.kr/B553881/newRegistInfoService"

# 데이터 가져오기 함수
def fetch_data(params):
    try:
        params['serviceKey'] = API_KEY  # 인코딩된 키 추가
        response = requests.get(ENDPOINT, params=params)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        return response.json()  # JSON 형식으로 데이터 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
 