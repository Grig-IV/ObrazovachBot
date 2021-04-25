from telebot import TeleBot

class LoggerBot:
    _bot_singelton = None
    _admin_id = None
    
    def create(bot_token, admin_id):
        if not LoggerBot._bot_singelton:
            LoggerBot._bot_singelton = TeleBot(bot_token)
            _admin_id = admin_id

        return LoggerBot._bot_singelton

    def get_bot():
        if not LoggerBot._bot_singelton:
            return Exception("LoggerBot not created yet")

        return LoggerBot._bot_singelton

    def send_log(self, package):
        LoggerBot._bot_singelton.send_message(LoggerBot._admin_id, "pass")