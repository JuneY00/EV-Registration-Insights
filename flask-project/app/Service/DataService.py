import pandas as pd
import os

class DataService:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_car_cnt(self, year, region):
        current_dir = os.path.dirname(__file__)
        csv_file_path = os.path.join(current_dir, 'electric_vehicles_data.csv')

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
