from telebot import types

from src.ArticleModul.articles_modul import ArticleModul
from src.Services.logger import Logger
# from src.Services.telebot_provider import TelebotProvider


class ObrazovachBot:
    def __init__(self, pikcher_storage, db_manager):
        self.pikcher_storage = pikcher_storage
        self.db_manager = db_manager

        self.moduls = list()
        self.article_modul = ArticleModul(self)
        self.moduls.append(self.article_modul)

        self._is_initialized = False

    def middleware_handler(self, package):
        if Logger.is_enabled:
            Logger.send_log(package)

        pikcher = self.pikcher_storage.get_or_create_user(package)

        is_bot_initialized = self.initialization_handler(pikcher, package)

        if is_bot_initialized and pikcher is not None:
            package.access_token = True
            package.pikcher = pikcher
        else:
            package.access_token = False

        return package

    def initialization_handler(self, pikcher, package):
        if self._is_initialized:
            return True

        if type(package) == types.CallbackQuery:
            _, _, db_message_id = package.data.split()
            self.load_db(pikcher.chat_id, db_message_id)
            self._is_initialized = True
        elif type(package) == types.Message:
            if package.text == '/skip_init':
                self._is_initialized = True
            else:
                pass

        return self._is_initialized

    def load_db(self, chat_id, db_message_id):
        db_dict = self.db_manager.load_db(chat_id, db_message_id)

        self.pikcher_storage.set_users_db(db_dict)
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
