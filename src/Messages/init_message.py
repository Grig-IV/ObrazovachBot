from src.AbstractClasses.abstract_message import Message


class InitMessage(Message):
    def __init__(self):
        text = "Сервер недавно перезапускался, нажимте обновить"
        super().__init__(text)
