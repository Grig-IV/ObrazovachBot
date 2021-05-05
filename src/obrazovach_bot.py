from telebot import types

from src.ArticleModul.articles_modul import ArticleModul
from src.Services.message_service import MessageService
from src.Messages.init_message import InitMessage
from src.Services.telebot_provider import TelebotProvider
from src.UserStorage.user_storage import UserStorage
from src.DatabaseManager.database_manager import DatabaseManager


class ObrazovachBot:
    def __init__(self, telebot, pikchers_names):
        self._is_initialized = False

        self.telebot = telebot

        self.moduls = list()
        self.article_modul = ArticleModul(self, telebot)
        self.moduls.append(self.article_modul)

        self.pikcher_storage = UserStorage(pikchers_names)
        self.db_manager = DatabaseManager(telebot)

    def initialization_handler(self, pikcher, package):
        if self._is_initialized:
            return True

        if type(package) == types.CallbackQuery:
            _, _, db_message_id = package.data.split()
            self.load_db(db_message_id)
            self._is_initialized = True
        elif type(package) == types.Message:
            if package.text == '/skip_init':
                self._is_initialized = True
            else:
                telebot = TelebotProvider.get_telebot()
                pass

        return self._is_initialized

    def load_db(self, chat_id, db_message_id):
        db_dict = self.db_manager.load_db(chat_id, db_message_id)

        self.pikchers_rep.set_pikchers_db(db_dict)
        for modul in self.moduls:
            modul.set_db(db_dict)

    def save_db(self):
        db_dict = dict()
        
        db_name, db = self.pikcher_storage.get_users_db()
        db_dict[db_name] = db
        for modul in self.moduls:
            db_name, db = modul.get_db()
            db_dict[db_name] = db

        pikchers = self.pikcher_storage.get_users()
        self.db_manager.save_db(pikchers, db_dict)

    def parse_command(self, command):
        if ' ' not in command:
            return command, None
        
        command, value = map(lambda s: s.strip(), command.split())
        return command, value



