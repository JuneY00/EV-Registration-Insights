import requests

class APIClient:
    @staticmethod
    def fetch_data(endpoint, api_key, params):
        try:
            params['apiKey'] = api_key
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
