from app.main.config.application_config import ApplicationConfig
from app.main.constant.static_constant import StaticConstant
from app.main.constant.default_constant import DefaultConstant
from app.main.strategy.signal_strategy import SignalStrategy
from app.main.bot.telegram_bot import TelegramBot
from app.main.util.file_handler_util import FileHandlerUtil
from app.main.util.log_util import LogUtil

import os.path
import time
import datetime
import calendar

class StrategyService():
    
    def __init__(self):
        #TG機器人
        self.bot = TelegramBot.bot
        pass
    
    def signal_notify(self, symbol=DefaultConstant.DEFAULT_SYMBOL, interval=DefaultConstant.DEFAULT_INTERVAL, end_time=None, receivers=None):
        #若沒有指定結束時間，則預設為現在時間
        end_time = self.__default_or_set_time(end_time)
        
        #若接收者參數沒有傳，則預設通知訂閱者檔案中的所有訂閱者
        receivers = self.__default_or_set_receivers(receivers)
            
        #使用策略分析並取得信號
        signal = 0
        try:
            signal = SignalStrategy(symbol, interval, end_time).signal_analyze_using_kd_macd()
        except Exception as e:
            raise Exception("取得訊號錯誤：" + str(e))
        
        #若非觀望訊號，則需要發送通知給訂閱者們
        try:
            self.__send_notification_if_signal_appear(symbol=symbol, interval=interval, end_time=end_time, receivers=receivers, signal=signal)
        except Exception as e:
            err_msg = "發送通知錯誤："+str(e)
            #寄通知發生錯誤不中止程式，只需寫log即可
            LogUtil.write_error_log_by_date([err_msg])
            
        return signal
    
    def __default_or_set_time(self, timestamp):
        if timestamp == None:
            timestamp = calendar.timegm(time.gmtime())
        return timestamp
    
    def __default_or_set_receivers(self, receivers):
        if receivers == None:
            #從靜態資源中讀取訂閱者名單
            try:
                receivers = FileHandlerUtil.readline_to_arr(
                    os.path.join(
                        ApplicationConfig.static_resource_path, 
                        StaticConstant.TELEGRAM_DEVELOPERS_FILE_NAME if ApplicationConfig.is_test 
                        else StaticConstant.TELEGRAM_SUBSCRIBERS_FILE_NAME
                    )
                )
            except Exception as e:
                raise Exception("讀取訂閱者列表檔案發生錯誤：" + str(e))
        return receivers
        
    def __send_notification_if_signal_appear(self, symbol, interval, end_time, receivers, signal):
        message = "" #內文
        signal_str = "買入訊號" if signal == 1 else "賣出訊號" if signal == -1 else "無訊號" #訊號的中文字串
        date_time_str = "" #日期時間的中文字串
        try:
            date_time_str = str(datetime.datetime.fromtimestamp(end_time))
        except Exception as e:
            raise Exception("timestamp轉換至datetime字串發生錯誤："+str(e))
        if signal != 0:
            message = ('Buy' if signal == 1 else 'Sell') + ' Signal for ' + symbol + "\n"
            message += 'On '+ date_time_str +', '
            message += 'the comprehensive technical analysis of '+ symbol +' has formed a ' + ('buy' if signal == 1 else 'sell') + ' signal!'
            message += 'Try to place the ' + ('long' if signal == 1 else 'close') + ' position for ' + symbol
            for receiver in set(receivers):
                self.bot.send_message(receiver, message)
                LogUtil.write_daily_log_by_date(["成功發送"+ symbol + "(" + interval + ")" + "在" + date_time_str + "的" + signal_str + "通知訂閱者：" + str(receiver)])
        else:
            message = symbol + "(" + interval + ")" + "在" + date_time_str +"未出現明顯買入賣出訊號，沈住氣，再等等！機會總會降臨的！"
            if ApplicationConfig.is_test:
                for receiver in set(receivers):
                    print(str(receiver))
                    self.bot.send_message(receiver, message)
            LogUtil.write_daily_log_by_date([message])
        