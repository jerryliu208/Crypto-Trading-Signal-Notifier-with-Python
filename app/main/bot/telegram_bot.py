from app.main.config.application_config import ApplicationConfig
from app.main.constant.static_constant import StaticConstant
from app.main.util.file_handler_util import FileHandlerUtil
from app.main.strategy.signal_strategy import SignalStrategy
import app.main.constant.command_handler_constant as CommandConstant

import os.path

import telebot

bot = telebot.TeleBot(ApplicationConfig.tg_bot_api_key)

@bot.message_handler(commands=[CommandConstant.HELP])
def help_handler(message):
    help_msg = ""
    help_msg += "/" + CommandConstant.SUBSCRIBE + " -> 用此指令訂閱通知，當交易訊號出現時機器人就會通知你喔！\n"
    help_msg += "/" + CommandConstant.SIGNAL + " -> 用此指令，可以主動查詢您輸入的交易對之訊號～"
    bot.reply_to(message, help_msg)

@bot.message_handler(commands=[CommandConstant.START, CommandConstant.SUBSCRIBE])
def start_handler(message):
    start_msg = "\n\n" + "使用 /" + CommandConstant.HELP + " 指令來了解機器人使用方式吧！"
    #讀檔取得所有訂閱者
    subscriber_list_file_name = ""
    if ApplicationConfig.is_test:
        subscriber_list_file_name = StaticConstant.TELEGRAM_DEVELOPERS_FILE_NAME
    else:
        subscriber_list_file_name = StaticConstant.TELEGRAM_SUBSCRIBERS_FILE_NAME
    subscriber_list_path = os.path.join(ApplicationConfig.static_resource_path, subscriber_list_file_name)
    subscribers = FileHandlerUtil.readline_to_arr(subscriber_list_path)
    
    #檢查此chat.id是否已訂閱，尚未訂閱則加入訂閱名單
    if str(message.chat.id) not in subscribers:
        FileHandlerUtil.create_file_and_write_text(subscriber_list_path, [message.chat.id])
        bot.reply_to(message, "歡迎訂閱我喔！我會在行情出現訊號時通知你喔！" + start_msg)
    else:
        bot.reply_to(message, "已經訂閱過了喔！" + start_msg)
        
@bot.message_handler(commands=[CommandConstant.SIGNAL])
def handle_symbol_command(message):
    reply_msg = "歡迎來到訊號查詢功能！\n請以 ' [交易對] , [時間週期] ' 格式回傳你想查詢訊號的交易對。" + "\n"
    reply_msg += "輸入格式的範例 => BTCUSDT, 1d"
    sent_msg = bot.send_message(message.chat.id, reply_msg)
    # 下個步驟讓使用者輸入交易對
    bot.register_next_step_handler(sent_msg, get_symbol_signal)
    
def get_symbol_signal(message):
    user_input_text_arr = message.text.replace(" ", "").split(",")
    # 確認使用者輸入格式正確
    if len(user_input_text_arr) != 2:
        bot.reply_to(message, "輸入格式錯誤！請參考 /" + CommandConstant.SIGNAL + " 指令的指示！")
        return
    # 取得使用者輸入的交易對和時間週期
    symbol, interval = user_input_text_arr[0].upper(), user_input_text_arr[1]
    # 查訊使用者input的訊號
    signal = None
    try:
        signal = SignalStrategy(symbol=symbol, interval=interval).signal_analyze_using_kd_macd()
    except Exception as e:
        bot.send_message(message.chat.id, "分析錯誤，請檢察輸入的交易對或時間週期是否正確。" + str(e) if ApplicationConfig.is_test else "")
        return
    # 在這裡加入您要查詢的資訊，並回傳給使用者
    reply = "您查詢的：" + symbol + "(" + interval +")" + "，目前訊號為：" + ("適合買入" if signal == 1 else "適合賣出" if signal == -1 else "適合觀望")
    bot.send_message(message.chat.id, reply)


class TelegramBot():
    
    bot = bot
    
    def __init__(self):
        pass