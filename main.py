import folium
import json

# 대한민국 지도 중앙 좌표 (서울 근처)
center_coords = [36.5, 127.5]

# Folium 지도 객체 생성
map_korea = folium.Map(location=center_coords, zoom_start=7)

# 병합된 GeoJSON 파일 경로 설정
geojson_path = 'korea_merged_provinces_fixed.geojson'

# 도별 색상 설정 (샘플 설정)
colors = {
    "서울특별시": "#FF6347",   # Tomato색
    "경기도": "#4682B4",       # Steel Blue색
    "전라북도": "#32CD32",     # Lime Green색
    "전라남도": "#FFD700",     # Gold색
    "경상북도": "#BA55D3",     # Medium Orchid색
    "경상남도": "#20B2AA",     # Light Sea Green색
    "충청북도": "#FF4500",     # Orange Red색
    "충청남도": "#8A2BE2",     # Blue Violet색
    "제주특별자치도": "#228B22", # Forest Green색
    "강원도": "#FF69B4",       # Hot Pink색
    "부산광역시": "#1E90FF",   # Dodger Blue색
    "대구광역시": "#FF8C00",   # Dark Orange색
    "광주광역시": "#DA70D6",   # Orchid색
    "대전광역시": "#7B68EE",   # Medium Slate Blue색
    "울산광역시": "#9932CC",   # Dark Orchid색
    "세종특별자치시": "#87CEEB" # Sky Blue색
}

# GeoJSON 파일 읽기
with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 도별로 GeoJSON 데이터에 색칠을 적용
for feature in geojson_data['features']:
    province_name = feature['properties']['sidonm']  # 도 이름을 가져옴
    
    print(province_name)
    # 도 이름에 맞는 색상을 가져옴
    color = colors.get(province_name, "#FFFFFF")  # 기본값은 흰색
    
    # 도별 경계선에 색을 입힌 폴리곤 추가
    folium.GeoJson(
        feature,
        style_function=lambda feature, color=color: {
            'fillColor': color,
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.6,
        }
    ).add_to(map_korea)

# 결과를 HTML 파일로 저장
map_korea.save('korea_colored_sample.html')

print("지도 파일이 생성되었습니다: korea_colored_sample.html")
