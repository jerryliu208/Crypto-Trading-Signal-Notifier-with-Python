from app.main.data.trading_data import TradingData

class AutoTrade():
    def __init__(self, is_test):
        self.is_test = is_test
        self.trading_data = TradingData(is_test)
        
    def auto_trade(self):
        # do sth here...
        return
        
    def run(self):
        try:
            self.auto_trade()
        except Exception as e:
            print("自動交易程式錯誤:"+str(e))
