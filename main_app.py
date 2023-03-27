from app.main.config.application_config import ApplicationConfig
from app.main.bot.telegram_bot import TelegramBot
from app.main.strategy.notice_strategy import NoticeStrategy
from app.main.util.log_util import LogUtil

from threading import Thread
import time

#test
from app.test.notice_strategy_test import NoticeStrategyTest

def bot_polling():
    TelegramBot().bot.polling()
    
def main():
    polling_thread = Thread(target = bot_polling)
    polling_thread.start()
    try:
        notice_strategy = NoticeStrategy("BTCUSD_PERP", "1d")
        while True:
            notice_strategy.check_signal_and_notify()
            time.sleep(5)
    except Exception as e:
        LogUtil.write_error_log_by_date([str(e)])
    polling_thread.join()
    
def test():
    t1 = Thread(target = bot_polling)
    t1.start()
    NoticeStrategyTest().test()
    t1.join()
    
if __name__ == "__main__":
    if ApplicationConfig.is_test:
        test()
    else:
        main()