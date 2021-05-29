class Logger:
    _tb = None
    _admin_id = None

    @property
    def is_enabled():
        return Logger._tb is not None

    def enable(telebot):
        Logger._tb = telebot

    def send_log(package):
        pass
