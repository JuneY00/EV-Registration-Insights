import geopandas as gpd
import folium
import json
import pandas as pd  # Pandas 임포트 추가
import branca.colormap as cm  # 색상맵을 위한 라이브러리

# GeoJSON 파일 경로
geojson_path = 'korea_dissolved_provinces_with_cities.geojson'

# GeoJSON 데이터를 GeoPandas로 읽기
gdf = gpd.read_file(geojson_path)

# 전기차 등록 대수 (예시 데이터로 각 도별 전기차 등록 대수를 가정)
ev_data = {
    "서울": 30000,
    "경기": 15000,
    "강원": 7000,
    "전북": 3000,
    "전남": 5000,
    "경북": 7000,
    "경남": 8000,
    "충북": 4000,
    "충남": 6000,
    "제주": 12000
}

# 전기차 등록 대수를 Pandas DataFrame으로 변환 (GeoPandas와 호환)
ev_df = pd.DataFrame(list(ev_data.items()), columns=['sidonm', 'ev_count'])

# GeoDataFrame에 전기차 등록 대수를 병합
gdf = gdf.merge(ev_df, on='sidonm')

# Folium 지도 생성
map_korea = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 색상 맵 설정 (전기차 등록 대수가 많을수록 진한 녹색)
colormap = cm.LinearColormap(colors=['lightgreen', 'green', 'darkgreen'],
                             vmin=gdf['ev_count'].min(),
                             vmax=gdf['ev_count'].max(),
                             caption="Electric Vehicle Registration by Province")

# 스타일 함수 정의 (녹색을 강하게 적용)
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
    gdf,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['sidonm', 'ev_count'], aliases=['Province', 'EV Registration'])
).add_to(map_korea)

# 지도에 색상 범례 추가
colormap.add_to(map_korea)

# 결과를 HTML 파일로 저장
map_korea.save('korea_ev_map_colored_advanced.html')

print("지도 파일이 생성되었습니다: korea_ev_map_colored_advanced.html")
