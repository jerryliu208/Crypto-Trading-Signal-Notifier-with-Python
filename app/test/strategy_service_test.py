from app.main.util.log_util import LogUtil
#service
from app.main.service.strategy_service import StrategyService

class StrategyServiceTest():
    def __init__(self):
        pass
    
    def test(self):
        print("------YOU ARE IN TEST MODE------")
        print("[INFO] If you want to run application by PROD mode, please modify the parameter 'mode' in config file which named 'application_config.py'.")
        print("--------------------------------")
        self.signal_notify_test()
    
    def signal_notify_test(self):
        test_result = []
        notify_service = StrategyService()
        
        try:
            test_result.append(notify_service.signal_notify("BTCUSDT", "1d", 1678464000) == 1) #2023/03/11
            test_result.append(notify_service.signal_notify("BTCUSDT", "1d", 1674748800) == -1) #2023/01/27
            test_result.append(notify_service.signal_notify(end_time=1674748800) == -1) #2023/01/27
        except Exception as e:
            print("test failed...")
            print("Exception occered: " + str(e))
            #LogUtil.write_error_log_by_date([str(e)])
            return False
        
        if len(set(test_result)) == 1 and True in set(test_result):
            print("test successed!")
            return True
        else:
            print("test failed...")
            return False