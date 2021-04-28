from telebot import types

from src.message_manager import MessageManager
from src.viewe.init_message import InitMessage


class Initializer:
    def __init__(self):
        self._is_initialized = False

    def initialization_handler(self, pikcher, package):
        if self._is_initialized:
            return
        
        if type(package) == types.Message:
            MessageManager.send_temporary_message(pikcher.chat_id, InitMessage())

    def __bool__(self):
        return self._is_initialized
