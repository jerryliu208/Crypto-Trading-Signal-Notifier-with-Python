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
            arr.append(line.replace("\n", ""))
        f.close
        return arr
    
    @staticmethod
    def create_file_and_write_text(file_path, contents):
        mode = 'w'
        if os.path.exists(file_path):
            mode = 'a'
        f = open(file_path, mode)
        for content in contents:
            f.write(str(content) + "\n")
        f.close()
        
    @staticmethod
    def delete_log_files_older_than(date_str):
        log_dir = os.path.join(ApplicationConfig.static_resource_path, "log_file")
        for file_name in os.listdir(log_dir):
            file_date = datetime.datetime.strptime(file_name.split("_")[0], "%Y-%m-%d")
            if file_date < datetime.datetime.strptime(date_str, "%Y-%m-%d"):
                file_path = os.path.join(log_dir, file_name)
                os.remove(file_path)