from app.main.config.application_config import ApplicationConfig
from app.main.util.log_util import LogUtil
from app.main.service.market_service import MarketService
from app.test.market_service_test import MarketServiceTest

def main():
    try:
        MarketService("BTCUSD_PERP", "1d").check_signal_and_send_email()
    except Exception as e:
        LogUtil.write_error_log_by_date([str(e)])
    
def test():
    MarketServiceTest().test()
    
    
if __name__ == "__main__":
    if ApplicationConfig.is_test:
        test()
    else:
	    main()