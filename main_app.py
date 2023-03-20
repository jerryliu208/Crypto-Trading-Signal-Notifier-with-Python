#service
from app.main.service.auto_trade import AutoTrade

def main():
    #test mode or not
    is_test = True
    
    auto_trade = AutoTrade(is_test)
    auto_trade.run()