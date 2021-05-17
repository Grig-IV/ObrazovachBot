import datetime as dt


class Article:
    """
    Class for contain an article data.
    """
    STR_DATETIME_FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, link, rubrics, header, published_str,
                 taken_by=None, is_for_poll=None, **kwargs):
        self._link = link
        self._type = link.split('/')[1]
        self._rubrics = set(rubrics)
        self._header = header
        dt_format = Article.STR_DATETIME_FORMAT
        self._published = dt.datetime.strptime(published_str, dt_format)

        self._taken_by = taken_by
        self._is_for_poll = is_for_poll

    @property
    def link(self):
        return self._link

    @property
    def url(self):
        return "https://nplus1.ru" + self._link

    @property
    def type(self):
        return self._type

    @property
    def rubrics(self):
        return self._rubrics.copy()

    @property
    def header(self):
        return self._header

    @property
    def published(self):
        return self._published

    @property
    def is_for_poll(self):
        return self._is_for_poll

    taken_by = property()

    @taken_by.getter
    def taken_by(self):
        return self._taken_by

    @taken_by.setter
    def taken_by(self, pikcher_name):
        self._taken_by = pikcher_name

    def use_for_poll(self):
        self._is_for_poll = True

    def dont_use_for_poll(self):
        self._is_for_poll = False

    def to_dict(self):
        dt_format = Article.STR_DATETIME_FORMAT
        article_dict = {
            'link': self.link,
            'rubrics': list(self.rubrics),
            'header': self.header,
            'published_str': self.published.strftime(dt_format),
            'taken_by': self.taken_by,
            'is_for_poll': self.is_for_poll
        }

        return article_dict
