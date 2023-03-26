from app.main.config.application_config import ApplicationConfig
from app.main.util.email_util import EmailUtil
from app.main.util.file_handler_util import FileHandlerUtil
from app.main.util.log_util import LogUtil

# package of comprehensive technical analysis
import talib
import numpy as np
# official package from Binance
from binance.cm_futures import CMFutures

import calendar
import time
import datetime
import os.path as path

class MarketService():
    """
    Constructor
    
    @param
    symbol (String):     合約名稱 ex: "BTCUSD_PERP"
    interval (String):   時間週期 ex: "1d"
    [date] (String):     指定日期，不傳默認為今日日期 ex: "2022/03/14"
    [is_test] (Boolean): 是否為測試環境，不傳默認為否
    """
    def __init__(self, symbol, interval, date = None, is_test = False):
        #是否為測試模式
        self.is_test = is_test
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
            self.end_time = calendar.timegm(time.gmtime())
        #從靜態資源中讀取訂閱者名單
        static_resource_path = ApplicationConfig.static_resource_path
        subscribers_file_name = ""
        try:
            if is_test:
                subscribers_file_name = FileHandlerUtil.readline_to_arr(path.join(static_resource_path, "developers.txt"))
            else:
                subscribers_file_name = FileHandlerUtil.readline_to_arr(path.join(static_resource_path, "subscribers.txt"))
        except Exception as e:
            raise Exception("讀取訂閱者列表檔案發生錯誤：" + str(e))
        
    """
    check_signal_and_send_email()
    
    description: 
    取得訊號後，若適合買入或賣出則發送email給名單中的所有人
    
    @param
    
    @return
    signal(Integer): 訊號 -> [ 1=買入訊號, -1=賣出訊號, 0=持倉觀望 ]
    """
    def check_signal_and_send_email(self):
        #取得訊號為何
        signal = 0
        try:
            signal = self.signal_analyze_using_kd_macd()
        except Exception as e:
            raise Exception(str(e))
        
        #發送email通知訂閱者們
        try:
            self.send_email_to_subscribers(signal)
        except Exception as e:
            raise Exception(str(e))
        
        return signal
    
    """
    send_email_to_subscribers()
    
    description: 
    若為買出或賣出訊號，則發送email給訂閱者們
    
    @param
    signal(Integer): 訊號 -> [ 1=買入訊號, -1=賣出訊號, 0=持倉觀望 ]
    """
    def send_email_to_subscribers(self, signal):
        #若非觀望訊號，則需要發送email通知訂閱者們
        if signal != 0: 
            subject = "" #標題
            message = "" #內文
            date_str = "" #日期字串
            try:
                date_str = str(datetime.date.fromtimestamp(self.end_time))
            except Exception as e:
                raise Exception("timestamp轉換至date發生錯誤："+str(e))
            #買入訊號
            if signal > 0:
                subject = 'Buy Signal for ' + self.symbol
                message = 'On '+date_str+', the comprehensive technical analysis of '+ self.symbol +' has formed a buy signal! Try to place the long position for ' + self.symbol
            #賣出訊號
            if signal < 0:
                subject = 'Sell Signal for ' + self.symbol
                message = 'On '+date_str+', the comprehensive technical analysis of '+ self.symbol +' has formed a sell signal! Try to close the long position for ' + self.symbol
            try:
                EmailUtil.batch_send_email(subject, message, self.subscribers)
                signal_str = ""
                if signal > 0: signal_str = "買入訊號" 
                else: signal_str = "賣出訊號"
                LogUtil.write_daily_log_by_date(["成功發送"+ self.symbol + signal_str + "email給以下訂閱者：" + str(self.subscribers)])
            except Exception as e:
                err_msg = "發送Email錯誤: "+str(e)
                #寄email發生錯誤不中止程式，只需寫log即可
                LogUtil.write_error_log_by_date([err_msg])
        else:
            LogUtil.write_daily_log_by_date(["今天是" + self.symbol + "平靜的一天，沈住氣，再等等！機會總會降臨的！"])
            pass
            
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
        #先取得近期的最高價、最低價、收盤價，後續拿來做指標的計算
        high_prices = [] #最高價
        low_prices = [] #最低價
        close_prices = [] #收盤價
        try:
            # 初始化 Binance 客戶端
            client = CMFutures()
            # 透過Binance 客戶端獲取 K 線數據
            klines = client.klines(self.symbol, self.interval, endTime = int(self.end_time)*1000, limit = 50)
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
        
    