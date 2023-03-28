from app.main.config.application_config import ApplicationConfig
from app.main.bot.telegram_bot import TelegramBot
from app.main.service.strategy_service import StrategyService
from app.main.util.log_util import LogUtil

from threading import Thread
import time

#test
from app.test.strategy_service_test import StrategyServiceTest

def bot_polling():
    TelegramBot().bot.polling()
    
def service():
    try:
        notify_service = StrategyService()
        while True:
            notify_service.signal_notify()
            time.sleep(60)
    except Exception as e:
        LogUtil.write_error_log_by_date([str(e)])
    
def main():
    polling_thread = Thread(target = bot_polling)
    polling_thread.start()
    service()
    polling_thread.join()
    
def test():
    StrategyServiceTest().test()
    
if __name__ == "__main__":
    if ApplicationConfig.is_test:
        test()
        main()
    else:
        main()