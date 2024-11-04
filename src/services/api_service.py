import requests

class APIService:
    @staticmethod
    def fetch_data(api_url):
        response = requests.get(api_url)
        return response.json() if response.status_code == 200 else None
