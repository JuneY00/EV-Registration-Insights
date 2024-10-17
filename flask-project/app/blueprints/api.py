from flask import Flask, jsonify, render_template, request
import requests
import pandas as pd
import os 
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# API 호출에 필요한 정보
ENDPOINT = "http://apis.data.go.kr/B553881/newRegistInfoService"


# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# electric_vehicles_data.csv 파일이 위치한 경로
csv_file_path = os.path.join(current_dir, '../electric_vehicles_data.csv')

# CSV 파일 읽기
PD_ELECTRIC_VEHICLES = pd.read_csv(csv_file_path)



# 데이터 가져오기 함수
def fetch_data(params):
    try:
        params['serviceKey'] = API_KEY  # 인코딩된 키 추가
        response = requests.get(ENDPOINT, params=params)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        return response.json()  # JSON 형식으로 데이터 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
 


def fetch_car_cnt(year, region):
    try:
        if region in [None, ''] :
            raise Exception(f"An error occurred: {str(e)}")

        filtered_df = PD_ELECTRIC_VEHICLES[PD_ELECTRIC_VEHICLES['region'] == region]
        
        if year == 'all':
            df = filtered_df.groupby(['year', 'region'])['cnt'].sum().reset_index()
            df = df.sort_values(['year', 'region'])
            df['month'] = None
        else:
            df = filtered_df[filtered_df['year'] == int(year)]
        
        df = df.rename(columns={'year': 'year', 'region': 'do', 'cnt': 'elecar_enroll_num'})
        
        result = df.to_dict('records')
        return result
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")



if __name__ == '__main__':
    fetch_car_cnt(2024)