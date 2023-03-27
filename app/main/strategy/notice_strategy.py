from app.main.config.application_config import ApplicationConfig
from app.main.constant.static_constant import StaticConstant
from app.main.bot.telegram_bot import TelegramBot
from app.main.util.file_handler_util import FileHandlerUtil
from app.main.util.log_util import LogUtil

# package of comprehensive technical analysis
import talib
import numpy as np
import ccxt

import requests
import json
import calendar
import time
import datetime
import os.path as path

class NoticeStrategy():
    """
    Constructor
    
    @param
    symbol (String):     合約名稱 ex: "BTCUSD_PERP"
    interval (String):   時間週期 ex: "1d"
    [date] (String):     指定日期，不傳默認為今日日期 ex: "2022/03/14"
    [is_test] (Boolean): 是否為測試環境，不傳默認為否
    """
    def __init__(self, symbol, interval, date = None):
        #是否為測試模式
        self.is_test = ApplicationConfig.is_test
        #欲分析行情之合約別
        self.symbol = symbol
        #時間週期
        self.interval = interval
        #指定日期
        if date != None:
            try:
                end_time = time.mktime(datetime.datetime.strptime(date, "%Y/%m/%d").timetuple())
                self.end_time = end_time
            except Exception as e:
                raise Exception("日期字串轉換為timestamp發生錯誤："+str(e))
        else:
            self.end_time = None
        #TG機器人
        self.bot = TelegramBot.bot
        #從靜態資源中讀取訂閱者名單
        static_resource_path = ApplicationConfig.static_resource_path
        subscribers_file_name = ""
        try:
            if self.is_test:
                subscribers_file_name = StaticConstant.TELEGRAM_DEVELOPERS_FILE_NAME
            else:
                subscribers_file_name = StaticConstant.TELEGRAM_SUBSCRIBERS_FILE_NAME
            self.subscribers = FileHandlerUtil.readline_to_arr(path.join(static_resource_path, subscribers_file_name))
        except Exception as e:
            raise Exception("讀取訂閱者列表檔案發生錯誤：" + str(e))
        
    """
    check_signal_and_notify()
    
    description: 
    取得訊號後，若適合買入或賣出則使用機器人發送通知給名單中的所有人
    
    @param
    
    @return
    signal(Integer): 訊號 -> [ 1=買入訊號, -1=賣出訊號, 0=持倉觀望 ]
    """
    def check_signal_and_notify(self):
        
        
        #取得訊號為何
        signal = 0
        try:
            signal = self.signal_analyze_using_kd_macd()
        except Exception as e:
            raise Exception(str(e))
        
        #發送通知給訂閱者們
        try:
            self.send_notification_to_subscribers(signal)
        except Exception as e:
            raise Exception(str(e))
        
        return signal
    
    """
    send_notification_to_subscribers()
    
    description: 
    若為買出或賣出訊號，則發送通知給訂閱者們
    
    @param
    signal(Integer): 訊號 -> [ 1=買入訊號, -1=賣出訊號, 0=持倉觀望 ]
    """
    def send_notification_to_subscribers(self, signal):
        date_time_str = ""
        try:
                date_time_str = str(datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())))
                if self.end_time != None:
                    date_time_str = str(datetime.datetime.fromtimestamp(self.end_time))
        except Exception as e:
            raise Exception("timestamp轉換至datetime發生錯誤："+str(e))
        #若非觀望訊號，則需要發送通知給訂閱者們
        if signal != 0: 
            subject = "" #標題
            message = "" #內文
            signal_str = "" #訊號的中文字串
            #買入訊號
            if signal > 0:
                signal_str = "買入訊號"
                subject = 'Buy Signal for ' + self.symbol
                message = 'On '+ str(date_time_str) +', the comprehensive technical analysis of '+ self.symbol +' has formed a buy signal! Try to place the long position for ' + self.symbol
            #賣出訊號
            if signal < 0:
                signal_str = "賣出訊號"
                subject = 'Sell Signal for ' + self.symbol
                message = 'On '+ str(date_time_str) +', the comprehensive technical analysis of '+ self.symbol +' has formed a sell signal! Try to close the long position for ' + self.symbol
            try:
                notify_msg = subject + "\n" + message
                for subscriber in set(self.subscribers):
                    self.bot.send_message(subscriber, notify_msg)
                    LogUtil.write_daily_log_by_date(["成功發送"+ self.symbol + "(" + self.interval + ")" + "在" + str(date_time_str) + "的" + signal_str + "通知訂閱者：" + str(subscriber)])
            except Exception as e:
                err_msg = "發送通知錯誤: "+str(e)
                #寄通知發生錯誤不中止程式，只需寫log即可
                LogUtil.write_error_log_by_date([err_msg])
        else:
            no_signal_msg = self.symbol + "(" + self.interval + ")" + "在" + str(date_time_str) +"未出現明顯買入賣出訊號，沈住氣，再等等！機會總會降臨的！"
            if self.is_test:
                for subscriber in set(self.subscribers):
                    print(str(subscriber))
                    self.bot.send_message(subscriber, no_signal_msg)
            LogUtil.write_daily_log_by_date([no_signal_msg])
            
    """
    signal_analyze_using_kd_macd()
    
    description: 
    使用KD指標搭配MACD指標檢查目前訊號型態，訊號條件如下
    -> 買入訊號：
        ---> KD指標：
        1. k值小於20
        2. k值大於d值
        ---> MACD指標：
        1. dif以及dea於零線之下
        2. dif於dea之下
        3. 柱狀圖即將由下向上穿過零線(我預設為柱狀圖 > -400)
        4. dif近兩日值相減之絕對值足夠小(我預設為 < 80)
    -> 賣出訊號：
        ---> KD指標：
        1. k值大於80
        2. k值小於d值
        ---> MACD指標：
        1. dif以及dea於零線之上
        2. 柱狀圖即將由上向下穿過零線(我預設為柱狀圖 < 400)
    
    @param
    
    return Integer: [ 1=買入訊號, -1=賣出訊號, 0=持倉觀望 ]
    """
    def signal_analyze_using_kd_macd(self):
        end_time = 0
        if self.end_time != None:
            end_time = self.end_time
        else:
            end_time = calendar.timegm(time.gmtime())
        #先取得近期的最高價、最低價、收盤價，後續拿來做指標的計算
        high_prices = [] #最高價
        low_prices = [] #最低價
        close_prices = [] #收盤價
        try:
            # 透過Binance API獲取 K 線數據
            url = "https://api.binance.us/api/v3/klines"
            # 設置請求參數
            params = {
                "symbol": self.symbol,
                "interval": self.interval,
                "limit": 50,
                "endTime": int(end_time)*1000
            }
            # 發送GET請求
            response = requests.get(url, params=params).json()
            klines = json.loads(str(response).replace("'", '"'))
            # 從K線數據中分別取出 最高價, 最低價, 收盤價
            for kline in klines:
                high_prices.append(float(kline[2]))
                low_prices.append(float(kline[3]))
                close_prices.append(float(kline[4]))
        except Exception as e:
            raise Exception("獲取/分析K線數據錯誤："+str(e))
        
        # 透過talib提供的函示取得 KD 指標和 MACD 指標
        slow_k, slow_d = talib.STOCH(np.array(high_prices), np.array(low_prices), np.array(close_prices), 
                                    fastk_period=14, slowk_period=1, slowk_matype=0, slowd_period=3, slowd_matype=0)
        dif, dea, macd = talib.MACD(np.array(close_prices), fastperiod=12, slowperiod=26, signalperiod=9)
        
        # 獲取最近的 KD 和 MACD 值
        last_k, last_d = slow_k[-1], slow_d[-1]
        last_dif, last_dea, last_macd = dif[-1], dea[-1], macd[-1]
        
        #-----買入訊號------
        #KD
        is_kd_below_twenty = last_k < 20 #k值小於20
        is_k_larger_than_d = last_k > last_d #k值大於d值
        #MACD
        is_dif_dea_below_zero = last_dif < 0 and last_dea < 0 #dif以及dea於零線之下
        is_dif_below_dea = last_dif < last_dea #dif於dea之下
        is_macd_crossing_above_zero = last_macd > -400 #柱狀圖即將由下向上穿過零線(我預設為柱狀圖 > -400)
        is_macd_dif_difference_is_small = (last_dif - dif[-2]) < -80 #dif近兩日值相減之絕對值足夠小(我預設為 < 80)
        
        #-----賣出訊號-----
        #KD
        is_kd_above_eighty = last_k > 80 #k值大於80
        is_k_less_than_d = last_k < last_d #k值小於d值
        #MACD
        is_dif_dea_above_zero = last_dif > 0 and last_dea > 0 #dif以及dea於零線之上
        is_macd_crossing_below_zero = last_macd < 400 #柱狀圖即將由上向下穿過零線(我預設為柱狀圖 < 400)
        
        # 判斷買入訊號是否皆達成
        if is_kd_below_twenty and is_k_larger_than_d and is_dif_dea_below_zero and is_dif_below_dea and is_macd_crossing_above_zero and is_macd_dif_difference_is_small:
            return 1
        # 判斷賣出訊號是否皆達成
        elif is_kd_above_eighty and is_k_less_than_d and is_dif_dea_above_zero and is_macd_crossing_below_zero:
            return -1
        else:
            return 0
        
    