from app.main.util.file_handler_util import FileHandlerUtil

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
        LogUtil.write_log_file(daily_log_arr)
    
    @staticmethod
    def write_error_log_by_date(err_log_arr):
        date_time_str_now = str(datetime.datetime.fromtimestamp(calendar.timegm(time.gmtime())))
        #err log content
        for index, err_log_text in enumerate(err_log_arr):
            err_log_arr[index] = date_time_str_now + " [ERROR]: " + err_log_text
        LogUtil.write_log_file(err_log_arr)
        
    @staticmethod
    def write_log_file(log_arr):
        #file name
        date_str_now = str(datetime.date.fromtimestamp(calendar.timegm(time.gmtime())))
        file_name = date_str_now + "_log.txt"
        
        FileHandlerUtil.create_file_and_write_text(os.path.join("log_file", file_name), log_arr)
        
    