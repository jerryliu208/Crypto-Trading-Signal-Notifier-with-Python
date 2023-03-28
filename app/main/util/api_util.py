import requests
import json

class ApiUtil():
    
    @staticmethod
    def get_api(url, params={}):
        try:
            raw_response = requests.get(url, params=params).json()
            response_data = json.loads(str(raw_response).replace("'", '"'))
        except Exception as e:
            raise Exception("GET請求發送或接收錯誤："+str(e))
        return response_data