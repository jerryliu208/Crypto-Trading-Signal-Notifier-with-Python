from app.main.config.application_config import ApplicationConfig

import os
import os.path
import datetime

class FileHandlerUtil():
    @staticmethod
    def readline_to_arr(path):
        arr = []
        f = open(path, 'r')
        for line in f.readlines():
            arr.append(line)
        f.close
        return arr
    
    @staticmethod
    def create_file_and_write_text(path, contents):
        file_path = os.path.join(ApplicationConfig.static_resource_path, path)
        mode = 'w'
        if len(FileHandlerUtil.readline_to_arr(file_path)) > 0:
            mode = 'a'
        f = open(file_path, mode)
        for content in contents:
            f.write(content + "\n")
        f.close()
        
        #清除一個月前的所有舊日誌檔
        one_month_ago_date_str = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        FileHandlerUtil.delete_log_files_older_than(one_month_ago_date_str)
        
    @staticmethod
    def delete_log_files_older_than(date_str):
        log_dir = os.path.join(ApplicationConfig.static_resource_path, "log_file")
        for file_name in os.listdir(log_dir):
            file_date = datetime.datetime.strptime(file_name.split("_")[0], "%Y-%m-%d")
            if file_date < datetime.datetime.strptime(date_str, "%Y-%m-%d"):
                file_path = os.path.join(log_dir, file_name)
                os.remove(file_path)