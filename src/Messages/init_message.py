from src.AbstractClasses.abstract_message import Message

class InitMessage(Message):
    def __init__(self):
        self.text = "Сервер недавно перезапускался, нажимте обновить"

    def get_kwargs(self):
        return {'text': self.text}