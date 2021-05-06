from src.ArticleModul.nplus1_parser import Parser_NP1
from src.ArticleModul.Models.article import Article


class ArticleDataBase:
    def __init__(self):
        self._last_update = None
        self._articles = list()

        self.filters = {'free_articles': lambda a: a.taken_by is None,
                        'taken_articles': lambda a: a.taken_by is not None}

    @property
    def last_update(self):
        return self._last_update

    def get_db(self):
        return list(map(lambda a: a.to_dict(), self._articles))

    def set_db(self, article_dict_list):
        self._articles = list(map(lambda d: Article(**d), article_dict_list))

    def get_articles(self, key_func=None):
        if key_func is None:
            return self._articles.copy()
        
        articles = list(filter(key_func, self._articles))
        return articles

    def find_article(self, article_url):
        for article in self._articles:
            if article.url == article_url:
                return article

        return None

    def update(self):
        links_on_main = Parser_NP1.get_links_on_main()
        db_links = map(lambda a: a.link, self._articles)
        new_links = list(filter(lambda l: l not in db_links, links_on_main))
        
        for link in new_links:
            article_dict = Parser_NP1.parse_article(link)
            article = Article(**article_dict)
            self._articles.append(article)
