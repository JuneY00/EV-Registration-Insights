from typing import Dict, List, Any, Optional
from Service.dataLoader import DataLoader 
from Service.evService import EVService
import os 
import csv

class EVController:
    # 각 route 요청 controller에서 처리 
    def __init__(self):        
        self.dataLoader = DataLoader()
        self.ev_service = EVService()
        self.all_ev_data = self.ev_service.get_ev_data()  # EV 데이터 가져오기
        
    def get_ev_info_all(self) -> list:
        """
        모든 EV 데이터에서 필요한 정보를 추출하여 반환

        :return: EV 데이터 리스트
        """
        results = []
        for data in self.all_ev_data:
            if 'ev_data' in data:
                results.append(data['ev_data'])

        return results
    
    def get_ev_info_charger_type(self) -> Dict[str, Dict[str,int]]:
        """
        각 지역별 EV 충전기 유형의 총합을 계산하여 반환

        :return: 지역별 충전기 유형 총합을 담은 딕셔너리
        """
        
        results: Dict[str, Dict[str, int]] = {}
        
        for item in self.all_ev_data:
            region = item.get('region')
            data = item.get('ev_data', [])
            
            rapid_total = sum(d.get('rapidCnt', 0) for d in data)  # rapidCnt 키가 없으면 0으로 처리
            slow_total = sum(d.get('slowCnt', 0) for d in data)    # slowCnt 키가 없으면 0으로 처리

            results[region] = {
                'rapidTotal': rapid_total,
                'slowTotal': slow_total
            }
        
        return results
    
    def get_location_and_draw_map(self) -> Dict[str, Dict[str, Any]]:
        """
        CSV 파일에서 도로명 주소를 읽어 위도 및 경도와 EV 데이터를 결합하여 반환

        :return: 도로명 주소를 키로 하고, 위도, 경도 및 EV 데이터를 담은 딕셔너리
        """

        file_path = os.path.join('app', 'Controller', 'stnAddr - stnAddr.csv')
        
        if os.path.exists(file_path):
            print(f"파일이 존재합니다: {file_path}")
            locations = self.dataLoader.read_csv_file(file_path)
                 
            address_dict = {}
            for location in locations:
                stnAddr = location['stnAddr']
                # print(location['latitude']ㄴ)
                
                address_dict[stnAddr]={
                    'latitude':location['latitude'],
                    'longitude':location['longitude']
                }
                
            results: Dict[str, Dict[str, Any]] = {}

            for item in self.all_ev_data:
                ev_data = item.get('ev_data',[])
            
                if isinstance(ev_data, list):
                    for data in ev_data:
                        stnAddr = data.get('stnAddr')

                        if stnAddr in address_dict:

                            latitude: Optional[float] = address_dict[stnAddr]['latitude']             
                            longitude: Optional[float] = address_dict[stnAddr]['longitude']
         
                            if latitude is not None and longitude is not None:  # 위도와 경도가 유효한지 확인
                                results[stnAddr] = {
                                    'latitude': latitude,
                                    'longitude': longitude,
                                    'ev_data': data
                                }
                            else:
                                print(f"위도 또는 경도가 없는 주소: {stnAddr}")
        else:
            print(f"파일이 존재하지 않습니다: {file_path}")        

        return results
