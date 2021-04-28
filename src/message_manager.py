class MessageManager:
    _bot = None
    _trach_can = list()

    def init(telebot):
        MessageManager._bot = telebot

    def send_message(chat_id, message):
        MessageManager._bot.send_message(chat_id, **message)

    def send_temporary_message(chat_id, message):
        mes = MessageManager._bot.send_message(chat_id,
                                               **message.get_kwargs())
        MessageManager._trach_can.append(mes)

    def del_temporary_messages():
        MessageManager._trach_can = list()
