from app.main.config.api_config import ApiConfig
from app.main.constant.api_constant import ApiConstant

class TradingData():
    def __init__(self, is_test):
        #base url
        if is_test:
            self.rest_base_url = ApiConstant.TEST_REST_BASE_URL
            self.web_socket_base_url = ApiConstant.TEST_WEB_SOCKET_BASE_URL
        else:
            self.rest_base_url = None
            self.web_socket_base_url = None
            
        #api key and secret key
        self.api_key = ApiConfig.api_key
        self.secret_key = ApiConfig.secret_key