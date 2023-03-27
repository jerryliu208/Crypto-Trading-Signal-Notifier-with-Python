from app.main.util.file_handler_util import FileHandlerUtil
from app.main.config.application_config import ApplicationConfig

import calendar
import time
import datetime
import os.path

class LogUtil():
    @staticmethod
    def write_daily_log_by_date(daily_log_arr):
        date_time_str_now = str(datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())))
        #daily log content
        for index, daily_log_text in enumerate(daily_log_arr):
            daily_log_arr[index] = date_time_str_now + " [LOG]: " + daily_log_text
        LogUtil.write_log_file_and_remove_old_file(daily_log_arr)
    
    @staticmethod
    def write_error_log_by_date(err_log_arr):
        date_time_str_now = str(datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())))
        #err log content
        for index, err_log_text in enumerate(err_log_arr):
            err_log_arr[index] = date_time_str_now + " [ERROR]: " + err_log_text
        LogUtil.write_log_file_and_remove_old_file(err_log_arr)
        
    @staticmethod
    def write_log_file_and_remove_old_file(log_arr):
        #file name
        date_str_now = str(datetime.date.fromtimestamp(calendar.timegm(time.gmtime())))
        file_name = date_str_now + "_log.txt"
        
        #寫檔案
        file_path = os.path.join(ApplicationConfig.static_resource_path, "log_file", file_name)
        FileHandlerUtil.create_file_and_write_text(file_path, log_arr)
        
        #清除一個月前的所有舊日誌檔
        one_month_ago_date_str = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        FileHandlerUtil.delete_log_files_older_than(one_month_ago_date_str)
        
    