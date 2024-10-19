from flask import jsonify, render_template
from app.model.ev_charge_service import EVChargeService
import json
import csv

class EVChargerLocation:
    # 도로명주소 위도, 경도로 바꾸는 클래스 
    # 도로명주소만 들어있는 파일 생성 후에 구글 스프레드시트 geoCode로 변경  

    ''' 
    def __init__(self):
        self.ev_service = EVChargeService()
    
    def get_ev_info_location(self):
        results = []  # 도로명 주소 리스트 초기화
        all_data = self.ev_service.get_ev_data()

        for item in all_data:
            ev_data = item['ev_data']
            if isinstance(ev_data, list):
                for data in ev_data:
                    stnAddr = data.get('stnAddr')
                    if stnAddr:  # stnAddr가 None이 아닌 경우에만 추가
                        results.append(stnAddr)

        return results  # 도로명 주소 리스트 반환
    
    def save_stnAddr_to_csv(self, stnAddr_list):
        filename='stnAddr.csv'

        # CSV 파일에 도로명주소 저장
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['도로명주소'])  # CSV의 첫 번째 줄에 헤더 추가
                
                for stnAddr in stnAddr_list:
                    print(stnAddr)
                    writer.writerow([stnAddr])  # 각 도로명주소를 새 행에 추가
                    
            print(f"도로명주소가 '{filename}' 파일에 저장되었습니다.")
            
        except Exception as e:
            print(f"파일을 열거나 작성하는 중 오류 발생: {e}")
            
    '''
    def read_csv_file(filename):
        locations = []
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    stnAddr = row['도로명주소'],
                    latitude = float(row['Latitude']),
                    longitude = float(row['Longitude']),
                    
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
    
#     def main(self):
#         results = self.get_ev_info_location(s)
#         print(results, type(results))
#         self.ev_controller.save_stnAddr_to_csv(results)


# if __name__ == "__main__":
#     ev_controller = EVChargerLocation()  # 클래스 인스턴스 생성
#     ev_controller.main()  # 메인 메소드 호출