from typing import Dict, List, Any, Optional

class EVService:
    
    def __init__(self):        
        from Model.evChargeModel import EVChargeModel  # 모듈 위치에 맞춰 import
        from Service.dataLoader import DataLoader  # 모듈 위치에 맞춰 import

        self.ev_model = EVChargeModel()
        self.dataLoader = DataLoader()

    def get_ev_data(self) -> List[Dict[str, Any]]:
        """
        지역별 EV 데이터를 가져오는 메서드

        :return: 지역, 위도, 경도 및 EV 데이터를 포함한 리스트
        """
        
        data = self.dataLoader.load_json_data('SidoCode.json')
        results = []
        
        for item in data:
            sido_code = item['code']
            ev_data = self.ev_model.fetch_ev_charge_data(sido_code)

            results.append({
                'region' : item['region'], 
                'latitude' : item['latitude'], 
                'longitude' : item['longitude'], 
                'ev_data' : ev_data})
            
        return results