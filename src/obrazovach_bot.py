from src.pikchers_rep import PikchersRep
from src.initializer import Initializer
from src.article_manager import ArticleManager
from src.message_manager import MessageManager


class ObrazovachBot:
    def __init__(self, telebot, pikchers_names):
        self.tb = telebot
        MessageManager.init(telebot)

        self.pikchers = PikchersRep(pikchers_names)
        self.initializer = Initializer()
        self.article_manager = ArticleManager()

    @property
    def is_initialized(self):
        return bool(self.initializer)



