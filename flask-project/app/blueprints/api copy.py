from flask import Flask, jsonify, render_template, request
import requests
import geopandas as gpd
import folium
import pandas as pd
import branca.colormap as cm
import os

# Flask 앱 설정
app = Flask(__name__)

# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(__file__)

# electric_vehicles_data.csv 파일 경로
csv_file_path = os.path.join(current_dir, '../ static/electric_vehicles_data.csv')

# CSV 파일 읽기
PD_ELECTRIC_VEHICLES = pd.read_csv(csv_file_path)

# GeoJSON 파일 경로
geojson_path = os.path.join(current_dir, 'static/korea_dissolved_provinces_with_cities.geojson')

# GeoJSON 데이터를 GeoPandas로 읽기
gdf = gpd.read_file(geojson_path)

# API로부터 전기차 등록 대수 데이터 가져오기
def fetch_car_cnt(year, region):
    try:
        if region in [None, '']:
            raise ValueError("Region cannot be empty")

        if region == 'all':
            if year != 'all':
                df = PD_ELECTRIC_VEHICLES[PD_ELECTRIC_VEHICLES['year'] == int(year)]
            else:
                df = PD_ELECTRIC_VEHICLES

            df = df.groupby(['year', 'region'])['cnt'].sum().reset_index()
            df = df.sort_values(['year', 'region'])
            df['month'] = None
        else:
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

# Folium 지도 생성 함수
def generate_map(ev_data):
    ev_data_dict = {item['do']: item['elecar_enroll_num'] for item in ev_data}
    
    # 전기차 등록 대수를 Pandas DataFrame으로 변환
    ev_df = pd.DataFrame(list(ev_data_dict.items()), columns=['sidonm', 'ev_count'])

    # GeoDataFrame에 전기차 등록 대수를 병합
    merged_gdf = gdf.merge(ev_df, on='sidonm')

    # Folium 지도 생성
    map_korea = folium.Map(location=[36.5, 127.5], zoom_start=7)

    # 색상 맵 설정 (전기차 등록 대수가 많을수록 진한 녹색)
    colormap = cm.LinearColormap(colors=['lightgreen', 'green', 'darkgreen'],
                                 vmin=merged_gdf['ev_count'].min(),
                                 vmax=merged_gdf['ev_count'].max(),
                                 caption="Electric Vehicle Registration by Province")

    def style_function(feature):
        ev_count = feature['properties']['ev_count']
        return {
            'fillColor': colormap(ev_count),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }

    # GeoDataFrame을 Folium 지도에 추가
    folium.GeoJson(
        merged_gdf,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['sidonm', 'ev_count'], aliases=['Province', 'EV Registration'])
    ).add_to(map_korea)

    colormap.add_to(map_korea)

    # 결과를 HTML 파일로 저장
    map_file = os.path.join(os.path.dirname(__file__), 'templates', 'korea_ev_map_colored_advanced.html')
    map_korea.save(map_file)
    return map_file

# 새 라우트 정의 - 연도에 따른 지도 생성 페이지
@app.route('/ev_map')
def ev_map():
    return render_template('ev_map_form.html')

# 새 라우트 정의 - 연도에 따른 지도 생성 처리
@app.route('/generate_map', methods=['POST'])
def generate_ev_map():
    selected_year = request.form.get('year')
    
    if selected_year:
        ev_data = fetch_car_cnt(selected_year, 'all')  # 모든 지역 데이터를 가져옴
        if ev_data:
            map_file = generate_map(ev_data)
            return render_template('korea_ev_map_colored_advanced.html')
    return "데이터를 불러오는 데 실패했습니다.", 500

if __name__ == '__main__':
    app.run(debug=True)
