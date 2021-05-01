class Logger:
    _tb = None
    _admin_id = None

    @property
    def is_enabled():
        return _tb != None

    def enable(telebot):
        LoggerBot._tb = telebot

    def send_log(package):
        pass