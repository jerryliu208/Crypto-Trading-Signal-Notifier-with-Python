from app.main.util.log_util import LogUtil
#service
from app.main.strategy.notice_strategy import NoticeStrategy

class NoticeStrategyTest():
    def __init__(self):
        pass
    
    def test(self):
        print("------YOU ARE IN TEST MODE------")
        print("[INFO] If you want to run application by PROD mode, please modify the parameter 'mode' in config file which named 'application_config.py'.")
        print("--------------------------------")
        self.check_signal_and_send_email_test()
    
    def check_signal_and_send_email_test(self):
        try:
            buy_signal = NoticeStrategy("BTCUSDT", "1d", "2023/03/11").check_signal_and_notify()
            sell_signal = NoticeStrategy("BTCUSDT", "1d", "2023/01/27").check_signal_and_notify()
            if buy_signal != 1 or sell_signal != -1:
                print("test failed...")
                return False
        except Exception as e:
            print("test failed...")
            print(str(e))
            #LogUtil.write_error_log_by_date([str(e)])
            return False
            
        print("test successed!")
        return True