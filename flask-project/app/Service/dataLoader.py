import os
import json
import csv
import requests
import pandas as pd
import os 
from flask import Flask, jsonify, render_template, request

class DataLoader:
    # JSON 파일에서 데이터 읽어오는 클래스
    @staticmethod
    def load_json_data(filename):
        file_path = os.path.join(os.path.dirname(__file__), filename)  
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        

    def fetch_car_cnt(year, region):
        # 현재 파일의 디렉토리 경로를 가져옴
        current_dir = os.path.dirname(__file__)

        # electric_vehicles_data.csv 파일이 위치한 경로
        csv_file_path = os.path.join(current_dir, 'electric_vehicles_data.csv')

        # CSV 파일 읽기
        PD_ELECTRIC_VEHICLES = pd.read_csv(csv_file_path)
        
        try:
            if region in [None, '']:
                raise ValueError("Region cannot be empty")

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


    
    def read_csv_file(self, filename):
        locations = []
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    stnAddr = row['도로명주소']
                    latitude = float(row['Latitude']) if row['Latitude'] else 0
                    longitude = float(row['Longitude']) if row['Longitude'] else 0

                    
                    # 위도와 경도가 모두 있는 경우만 추가
                    if latitude is not None and longitude is not None:
                        locations.append({
                            'stnAddr': stnAddr,
                            'latitude': latitude,
                            'longitude': longitude,
                        })
                    else:
                        print(f"위도 또는 경도가 없는 주소: {stnAddr}")
       
                except ValueError:
                    print(f"위도 또는 경도가 잘못된 형식입니다: {row['위도']}, {row['경도']}")
                except Exception as e:
                    print(f"오류 발생: {e}")
         
        return locations
