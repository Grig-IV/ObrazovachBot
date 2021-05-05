class TelebotProvider:
    _tb = None
    
    def set_telebot(telebot):
        TelebotProvider._tb = telebot

    def get_telebot():
        return TelebotProvider._tb
