import os
import json
import csv

class FileLoader:
    @staticmethod
    def load_json_data(filename):
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def read_csv_file(filename):
        locations = []
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    stnAddr = row['도로명주소']
                    latitude = float(row['Latitude'])
                    longitude = float(row['Longitude'])

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
