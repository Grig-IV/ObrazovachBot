import asyncio
import datetime as dt

from src.ArticleModule.nplus1_parser import Parser_NP1
from src.ArticleModule.Models.article import Article


class ArticleDataBase:
    def __init__(self):
        self._last_update = None
        self._free_articles = set()
        self._taken_articles = set()

    @property
    def last_update(self):
        return self._last_update

    @property
    def free_articles(self):
        return self._free_articles.copy()

    @property
    def taken_articles(self):
        return self._taken_articles.copy()

    @property
    def all_articles(self):
        return set.union(self.free_articles, self.taken_articles)

    def get_db(self):
        free_articles = list(map(lambda a: a.to_dict(), self.free_articles))
        taken_articles = list(map(lambda a: a.to_dict(), self.taken_articles))
        db = {'freeArticles': free_articles, 'takenArticles': taken_articles}
        return db

    def set_db(self, db):
        free_articles = map(lambda d: Article(**d), db['freeArticles'])
        taken_articles = map(lambda d: Article(**d), db['takenArticles'])
        self._free_articles = set(free_articles)
        self._taken_articles = set(taken_articles)

    def find_article(self, article_url):
        finding_g = (a for a in self.all_articles if a.url == article_url)
        return next(finding_g, None)

    async def update(self):
        MSK_TZ = dt.timezone(dt.timedelta(hours=3))
        self._last_update = dt.datetime.now(MSK_TZ)

        links_on_main = Parser_NP1.get_links_on_main()
        db_links = map(lambda a: a.link, self.all_articles)
        new_links = list(filter(lambda l: l not in db_links, links_on_main))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        tasks = list()
        for link in new_links:
            task = asyncio.create_task(Parser_NP1.parse_article(link))
            task = loop.create_task(Parser_NP1.load_page(link))
            tasks.append(task)
        load_pages = loop.run_until_complete(asyncio.gather(*tasks))

        article_dicts = await asyncio.gather(*tasks)

        article_dicts = map(lambda p: Parser_NP1.parse_page(p), load_pages)
        for a_dict in article_dicts:
            article = Article(**a_dict)
            self._free_articles.add(article)

    def move_from_free_to_taken(self, article):
        if article in self._free_articles:
            return

        self._free_articles.remove(article)
        self._taken_articles.add(article)

    def move_from_taken_to_free(self, article):
        if article in self._taken_articles:
            return

        self._taken_articles.remove(article)
        self._free_articles.add(article)
