from datetime import datetime 


class Article:
    """
    Class for contain an article data.
    """
    def __init__(self, link, rubrics, header, published_str,
                 taken_by=None, is_for_poll=None):
        self._link = link
        self._type = link.split('/')[1]
        self._rubrics = set(rubrics)
        self._header = header
        self._published = datetime.strptime(published_str, '%Y-%m-%d %H:%M')

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
        article_dict = {
            'link': self.link,
            'type': self.type,
            'rubrics': list(self.rubrics),
            'header': self.header,
            'published_str': self.published.strftime('%Y-%m-%d %H:%M'),
            'taken_by': self.taken_by,
            'is_for_poll': self.is_for_poll
        }

        return article_dict
