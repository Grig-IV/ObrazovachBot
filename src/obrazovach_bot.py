from telebot import TeleBot

from src.logger import LoggerBot
from src.pikchers_rep import PikchersRep
from src.initializer import Initializer
from src.article_manager import ArticleManager


class ObrazovachBot:
    def __init__(self, project_state, bot_token, pikchers_names, admin_id,
                 test_bot_token=None, logger_bot_token=None):
        self._project_state = project_state
        if project_state == "Development":
            test_bot_token = test_bot_token or bot_token
            self.tb = TeleBot(test_bot_token)
        elif project_state == "Production":
            self.tb = TeleBot(bot_token)

        self.logger = LoggerBot.create(logger_bot_token, admin_id)
        self.pikchers = PikchersRep(pikchers_names)
        self.initializer = Initializer()
        self.article_manager = ArticleManager()

    @property
    def is_development(self):
        return self._project_state == "Development"


