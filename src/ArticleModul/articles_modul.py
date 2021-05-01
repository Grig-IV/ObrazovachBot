from src.article_database import ArticleDataBase
from src.message_manager import MessageManager
from src.messages.alredy_taken_message import AlredyTakenWarning


class ArticleModul:
    def __init__(self, pikchers_repository):
        self.article_db = ArticleDataBase()
        self.pikchers_rep = pikchers_repository

    @update_messages
    @update_article_db
    def take_article(self, pikcher, article_url):
        article = self.article_db.get_article(article_url)

        if article.taken_by:
            return AlredyTakenWarning()

        article.taken_by = pikcher.username

    @update_messages
    @update_article_db
    def take_poll(self, pikcher, article):
        pass

    @update_messages
    def give_article_back(self, pikcher, article):
        pass

    def update_db_messages(self):
        pass
    
    def update_article_messages(self):
        pass

    # Decorators
    def update_article_db(func):
        def func_with_updater(self, *args, **kwargs):
            self.article_db.update()
            func(*args, **kwargs)
        return func_with_updater
        
    def update_messages(func):
        def func_with_updater(self, *args, **kwargs):
            func(*args, **kwargs)
            self.update_db_messages()
            self.update_article_messages()
        return func_with_updater
