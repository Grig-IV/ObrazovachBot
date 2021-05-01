from src.telebot_provider import TelebotProvider

class MessageManager:
    _tb = TelebotProvider.get_telebot()
    _trach_can = list()

    def send_message(chat_id, message):
        MessageManager._tb.send_message(chat_id, **message)


    def send_temporary_message(chat_id, message):
        mes = MessageManager._tb.send_message(chat_id,
                                              **message.get_kwargs())
        MessageManager._trach_can.append(mes)


    def del_temporary_messages():

        MessageManager._trach_can = list()

