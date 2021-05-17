import asyncio

from src.ArticleModul.article_database import ArticleDataBase
from src.Services.telebot_provider import TelebotProvider
from src.ArticleModul.Messages.article_message import ArticleMessage


class ArticleModul:
    def __init__(self, obrz_bot):
        self.obrz_bot = obrz_bot
        self.article_db = ArticleDataBase()

    def get_db(self):
        return 'articleModul', self.article_db.get_db()

    def set_db(self, dict_db):
        self.article_db.set_db(dict_db['articleModul'])

    # region Decorators
    def update_article_db(func):
        def func_with_updater(self, *args, **kwargs):
            asyncio.run(self.article_db.update())
            func(self, *args, **kwargs)

        return func_with_updater

    def update_messages(func):
        def func_with_updater(self, *args, **kwargs):
            func(self, *args, **kwargs)

            # update db messages
            self.obrz_bot.save_db()

            # update article messages
            pikchers_f = lambda p: p.data['articleMessageId'] is not None
            pikchers = self.obrz_bot.pikcher_storage.get_users(pikchers_f)
            for pikcher in pikchers:
                self.update_article_message(pikcher)

        return func_with_updater
    # endregion

    @update_messages
    @update_article_db
    def create_article_message(self, pikcher):
        a_mes = ArticleMessage(pikcher,
                               self.article_db.free_articles,
                               self.article_db.last_update)

        telebot = TelebotProvider.get_telebot()
        mes = telebot.send_message(pikcher.chat_id, **a_mes.get_kwargs())
        pikcher.set_data('articleMessageId', mes.message_id)

    # Message commands
    @update_messages
    @update_article_db
    def take_article(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)

        article.taken_by = pikcher.username

    @update_messages
    @update_article_db
    def take_poll(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)

        article.use_for_poll()

    @update_messages
    def give_article_back(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)

        if article.taken_by is not None:
            article.taken_by = None
        elif article.is_for_poll:
            article.dont_use_for_poll()

    def update_article_message(self, pikcher):
        a_mes = ArticleMessage(pikcher,
                               self.article_db.free_articles,
                               self.article_db.last_update)

        telebot = TelebotProvider.get_telebot()
        a_message_id = pikcher.data['articleMessageId']
        telebot.edit_message_text(chat_id=pikcher.chat_id,
                                  message_id=a_message_id,
                                  **a_mes.get_kwargs())

    # Callback action
    def switch_page(self, pikcher, numb_page):
        pikcher.set_data("currentPage", numb_page)
        self.update_article_message(pikcher)

    def switch_article_type(self, pikcher, article_type):
        pikcher.set_data("currArticleTypeShow", article_type)
        self.update_article_message(pikcher)
