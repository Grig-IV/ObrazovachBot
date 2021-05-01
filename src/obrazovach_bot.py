from telebot import types

from src.ArticleModul.articles_modul import ArticleModul
from src.Services.message_service import MessageService
from src.Messages.init_message import InitMessage


class ObrazovachBot:
    def __init__(self, telebot, pikchers_names):
        self._is_initialized = False

        self.moduls = list()
        article_modul = ArticleModul(telebot)
        self.moduls.append(article_modul)

        self.pikchers_rep = PikchersRep(pikchers_names)
        self.db_manager = DatabaseManager(telebot)

    def initialization_handler(self, pikcher, package):
        if self._is_initialized:
            return True
        
        # TODO: сделать обработку пустой инициализации

        if type(package) == types.Message:
            MessageService.send_temporary_message(pikcher.chat_id,
                                                  InitMessage())
            return False
        elif type(package) == types.CallbackQuery:
            _, _, db_message_id = package.data.split()
            self.load_db(db_message_id)
            return True

    def load_db(self, db_message_id):
        db_dict = self.db_manager.load_db(db_message_id)

        self.pikchers_rep.set_pikchers_db(db_dict)
        for modul in self.moduls:
            modul.set_db(db_dict)

    def save_db(self):
        db_dict = dict()
        
        db_name, db = self.pikchers_rep.get_pikchers_db()
        db_dict[db_name] = db
        for modul in self.moduls:
            db_name, db = modul.get_db()
            db_dict[db_name] = db

        pikchers = self.pikchers_rep.pikchers
        self.db_manager.save_db(pikchers, db_dict)

