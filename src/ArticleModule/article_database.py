import asyncio
import datetime as dt

from src.ArticleModule.nplus1_parser import Parser_NP1
from src.ArticleModule.Models.article import Article


class ArticleDataBase:
    FREE_ARTICLES_CAPACITY = 48
    TAKEN_ARTICLES_CAPACITY = 36

    def __init__(self):
        self._last_update = None

        # _free_articles: key=rubric, value=articl_list_of_rubric
        self._free_articles = dict()
        self._taken_articles = list()

    @property
    def last_update(self):
        return self._last_update

    @property
    def free_articles(self):
        free_articles_set = set()
        for articl_list in self._free_articles.values():
            free_articles_set.update(articl_list)
        return free_articles_set

    @property
    def taken_articles(self):
        return set(self._taken_articles)

    @property
    def all_articles(self):
        return set.union(self.free_articles, self.taken_articles)

    def get_db(self):
        free_articles = list(map(lambda a: a.to_dict(), self.free_articles))
        taken_articles = list(map(lambda a: a.to_dict(), self.taken_articles))
        db = {'freeArticles': free_articles, 'takenArticles': taken_articles}
        return db

    def set_db(self, db):
        taken_articles = map(lambda d: Article(**d), db['takenArticles'])
        self._taken_articles = list(taken_articles)

        free_articles = map(lambda d: Article(**d), db['freeArticles'])
        for a in free_articles:
            self._add_free_article(a)

    def update(self):
        MSK_TZ = dt.timezone(dt.timedelta(hours=3))
        self._last_update = dt.datetime.now(MSK_TZ)

        links_on_main = Parser_NP1.get_links_on_main()
        db_links = set(map(lambda a: a.link, self.all_articles))
        new_links = set.difference(links_on_main, db_links)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        tasks = list()
        for link in new_links:
            task = loop.create_task(Parser_NP1.load_page(link))
            tasks.append(task)
        load_pages = loop.run_until_complete(asyncio.gather(*tasks))

        loop.close()

        article_dicts = map(lambda p: Parser_NP1.parse_page(p), load_pages)
        for a_dict in article_dicts:
            article = Article(**a_dict)
            self._add_free_article(article)

        return bool(new_links)

    def find_article(self, article_url):
        finding_g = (a for a in self.all_articles if a.url == article_url)
        return next(finding_g, None)

    def move_from_free_to_taken(self, article):
        if article in self._taken_articles:
            print("Article alredy taken!")
            return

        self._remove_free_article(article)
        self._taken_articles.insert(0, article)

        # remove extra article
        capacity = ArticleDataBase.TAKEN_ARTICLES_CAPACITY
        while len(self._taken_articles) > capacity:
            self._taken_articles.pop()

    def move_from_taken_to_free(self, article):
        if article in self._free_articles:
            print("Article alredy free!")
            return

        self._taken_articles.remove(article)
        self._add_free_article(article)

    def _add_free_article(self, article):
        for r in article.rubrics:
            if r not in self._free_articles:
                self._free_articles[r] = list()

            self._free_articles[r].insert(0, article)

            # remove extra article
            capacity = ArticleDataBase.FREE_ARTICLES_CAPACITY
            while len(self._taken_articles) > capacity:
                self._taken_articles.pop()

    def _remove_free_article(self, article):
        for r in article.rubrics:
            if article not in self._free_articles[r]:
                continue

            self._free_articles[r].remove(article)
