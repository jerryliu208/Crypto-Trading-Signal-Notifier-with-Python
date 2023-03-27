from app.main.config.application_config import ApplicationConfig
from app.main.constant.static_constant import StaticConstant
from app.main.util.file_handler_util import FileHandlerUtil

import os.path

import telebot

bot = telebot.TeleBot(ApplicationConfig.tg_bot_api_key)

@bot.message_handler(commands=['start', 'subscirbe'])
def subscirbe(message):
    subscriber_list_file_name = ""
    if ApplicationConfig.is_test:
        subscriber_list_file_name = StaticConstant.TELEGRAM_DEVELOPERS_FILE_NAME
    else:
        subscriber_list_file_name = StaticConstant.TELEGRAM_SUBSCRIBERS_FILE_NAME
    subscriber_list_path = os.path.join(ApplicationConfig.static_resource_path, subscriber_list_file_name)
    subscribers = FileHandlerUtil.readline_to_arr(subscriber_list_path)
    if str(message.chat.id) not in subscribers:
        FileHandlerUtil.create_file_and_write_text(subscriber_list_path, [message.chat.id])
        bot.reply_to(message, "歡迎訂閱我喔！我會在行情出現訊號時通知你喔！")
    else:
        bot.reply_to(message, "已經訂閱過了喔！")

    

class TelegramBot():
    
    bot = bot
    
    def __init__(self):
        pass