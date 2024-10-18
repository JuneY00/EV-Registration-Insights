from flask import Flask, jsonify, request
import requests
import os 

# 데이터 가져오기 함수
def fetch_data(endpoint, api_key, params):
    try:
        params['apiKey'] = api_key
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        return response.json()  # JSON 형식으로 데이터 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
