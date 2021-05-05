from src.ArticleModul.article_database import ArticleDataBase
from src.Services.telebot_provider import TelebotProvider
from src.ArticleModul.Messages.article_message import ArticleMessage


class ArticleModul:
    def __init__(self, obrz_bot, pikchers_repository):
        self.obrz_bot = obrz_bot
        self.article_db = ArticleDataBase()

    def get_db(self):
        return 'articleModul', 'Test'
   
    def create_article_message(self, pikcher):
        telebot = TelebotProvider.get_telebot()

        a_mes = ArticleMessage()

        telebot.send_message(pikcher.chat_id, **a_mes.get_kwargs())


    # Decorator
    def update_article_db(func):
        def func_with_updater(self, *args, **kwargs):
            self.article_db.update()
            func(*args, **kwargs)

        return func_with_updater
    
    # Decorator
    def update_messages(func):
        def func_with_updater(self, *args, **kwargs):
            func(*args, **kwargs)
            self.obrz_bot.save_db()

            pikchers_f = lambda p: p.article_message_id is not None
            pikchers = self.obrz_bot.pikchers_rep.get_pikchers(pikchers_f)

            free_articles_f = lambda a: a.taken_by is None
            free_a = self.article_db.get_articles(free_articles_f)

            telebot = TelebotProvider.get_telebot()
            for p in pikchers:
                a_mes = ArticleMessage(p, free_a, None)
                telebot.edit_message(p.chat_id,
                                     p.article_message_id,
                                     **a_mes.get_kwargs())

        return func_with_updater

    @update_messages
    @update_article_db
    def take_article(self, pikcher, article_url):
        article = self.article_db.get_article(article_url)

        article.taken_by = pikcher.username

    @update_messages
    @update_article_db
    def take_poll(self, pikcher, article):
        article = self.article_db.get_article(article_url)

        article.use_for_poll()

    @update_messages
    def give_article_back(self, pikcher, article):
        article = self.article_db.get_article(article_url)

        if article.taken_by is not None:
            article.taken_by = None
        elif article.for_poll:
            article.dont_use_for_poll()
