from src.ArticleModul.article_database import ArticleDataBase
from src.Services.telebot_provider import TelebotProvider
from src.ArticleModul.Messages.article_message import ArticleMessage


class ArticleModul:
    def __init__(self, obrz_bot, pikchers_repository):
        self.obrz_bot = obrz_bot
        self.article_db = ArticleDataBase()

    def get_db(self):
        return 'articleModul', self.article_db.get_db()

    def set_db(self, dict_db):
        self.article_db.set_db(dict_db['articleModul'])

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

            free_articles_filter = self.article_db.filters['free_articles']
            free_articles = self.article_db.get_articles(free_articles_filter)

            telebot = TelebotProvider.get_telebot()
            for pikcher in pikchers:
                a_mes = ArticleMessage(pikcher,
                                       free_articles,
                                       self.article_db.last_update)
                telebot.edit_message(pikcher.chat_id,
                                     pikcher.article_message_id,
                                     **a_mes.get_kwargs())

        return func_with_updater

    @update_messages
    @update_article_db
    def create_article_message(self, pikcher):            
        free_articles_filter = self.article_db.filters['free_articles']
        free_articles = self.article_db.get_articles(free_articles_filter)
        a_mes = ArticleMessage(pikcher,
                               free_articles,
                               self.article_db.last_update)

        telebot = TelebotProvider.get_telebot()
        telebot.send_message(pikcher.chat_id, **a_mes.get_kwargs())

    @update_messages
    @update_article_db
    def take_article(self, pikcher, article_url):
        article = self.article_db.find_article(article_url)

        article.taken_by = pikcher.username

    @update_messages
    @update_article_db
    def take_poll(self, pikcher, article):
        article = self.article_db.find_article(article_url)

        article.use_for_poll()

    @update_messages
    def give_article_back(self, pikcher, article):
        article = self.article_db.find_article(article_url)

        if article.taken_by is not None:
            article.taken_by = None
        elif article.is_for_poll:
            article.dont_use_for_poll()
