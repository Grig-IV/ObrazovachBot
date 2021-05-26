import asyncio

from src.ArticleModule.article_database import ArticleDataBase
from src.Services.telebot_provider import TelebotProvider
from src.ArticleModule.Messages.article_message import ArticleMessage


class ArticleModule:
    def __init__(self, obrz_bot):
        self.obrz_bot = obrz_bot
        self.article_db = ArticleDataBase()

    # region Database manipulation
    def get_db(self):
        return 'articleModule', self.article_db.get_db()

    def set_db(self, dict_db):
        self.article_db.set_db(dict_db['articleModule'])
    # endregion

    # region Decorators
    def update_article_db_triger(func):
        def func_with_updater(self, *args, **kwargs):
            self.update_article_db()
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
    @update_article_db_triger
    def create_article_message(self, pikcher):
        a_mes = ArticleMessage(pikcher,
                               self.article_db.free_articles,
                               self.article_db.last_update)

        telebot = TelebotProvider.get_telebot()
        mes = telebot.send_message(pikcher.chat_id, **a_mes.get_kwargs())
        pikcher.set_data('articleMessageId', mes.message_id)

        # Message commands
    @update_messages
    @update_article_db_triger
    def take_article(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)
        if article is None:
            print("Article not found!")
            return

        article.taken_by = pikcher.username
        self.article_db.move_from_free_to_taken(article)

    @update_messages
    @update_article_db_triger
    def take_poll(self, article_url):
        article = self.article_db.find_article(article_url)
        if article is None:
            print("Article not found!")
            return

        article.use_for_poll()

    @update_messages
    @update_article_db_triger
    def give_article_back(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)
        if article is None:
            print("Article not found!")
            return

        if article.taken_by is not None:
            article.taken_by = None
            self.article_db.move_from_taken_to_free(article)
        elif article.is_for_poll:
            article.dont_use_for_poll()

    def update_article_message(self, pikcher):
        if self.article_db.last_update is None:
            self.update_article_db()

        a_mes = ArticleMessage(pikcher,
                               self.article_db.free_articles,
                               self.article_db.last_update)

        telebot = TelebotProvider.get_telebot()
        a_message_id = pikcher.data['articleMessageId']
        telebot.edit_message_text(chat_id=pikcher.chat_id,
                                  message_id=a_message_id,
                                  **a_mes.get_kwargs())
    # endregion

    # region Callback action
    def switch_page(self, pikcher, numb_page):
        if pikcher.data['currentPage'] == numb_page:
            self.update_article_db()

        pikcher.set_data("currentPage", numb_page)
        self.update_article_message(pikcher)

    def switch_article_type(self, pikcher, article_type):
        if pikcher.data['currArticleTypeShow'] == article_type:
            self.update_article_db()

        pikcher.set_data("currArticleTypeShow", article_type)
        pikcher.set_data("currentPage", 0)
        self.update_article_message(pikcher)

    def update_article_db(self):
        asyncio.run(self.article_db.update())
    # endregion
