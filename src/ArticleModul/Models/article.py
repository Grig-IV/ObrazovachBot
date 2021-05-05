# TODO: Перенести создание новости по ссылки в парсер

class _Article:
    """
    Class for contain an article data.
    """
    # Exemplars creators
    @staticmethod
    def _create(link, rubrics, header, publish_datetime):
        a = _Article()
        a._link = link
        a._kind = link.split('/')[1]
        a._rubrics = set(rubrics)
        a._header = header
        a._published = publish_datetime

        a._taken_by = None
        a._use_for_poll = False

        return a

    @staticmethod
    def create_by_dict(article_dict):
        link = article_dict['link']
        rubrics = article_dict['rubrics']
        header = article_dict['header']
        published_dt = dt.datetime.strptime(article_dict['published'],
                                            '%Y-%m-%d %H:%M')

        article = _Article._create(link, rubrics, header, published_dt)

        if article_dict.get('poll'):
            article._use_for_poll = article_dict.get('poll')
        if article_dict.get('taken_by'):
            article._taken_by = article_dict.get('taken_by')

        return article

    @staticmethod
    def create_by_link(article_link):
        """
        Parse article date from link and create Article object with the date.
        """
        article_page = requests.get("https://nplus1.ru" + article_link)
        if article_page.status_code != 200:
            return None
        article_html = BeautifulSoup(article_page.text, 'html.parser')

        rubrics_tags_table = article_html.select("p.table a[data-rubric]")
        if rubrics_tags_table:
            rubrics_list = map(lambda a: a['data-rubric'], rubrics_tags_table)
        else:
            rubrics_list = ['none']

        pb_date_str = article_html.select_one("div.meta time")['content']  # YYYY-MM-DD
        pb_time_str = article_html.select_one("div.meta time > span").get_text()  # HH:MM
        pb_datetime_str = pb_date_str + ' ' + pb_time_str
        pb_datetime = dt.datetime.strptime(pb_datetime_str, '%Y-%m-%d %H:%M')

        article_header = article_html.select_one("header h1").get_text()
        article_kind = article_link.split('/')[1]
        if article_kind == "material":
            subtitle = article_html.select_one("p.subtitle").get_text()
            article_header = "{0} | {1}".format(article_header, subtitle)

        return _Article._create(article_link, rubrics_list,
                                article_header, pb_datetime)

    # Data acces methods
    @property
    def link(self):
        return self._link

    @property
    def url(self):
        return "https://nplus1.ru" + self._link

    @property
    def type(self):
        return self._kind

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
    def for_poll(self):
        return self._use_for_poll

    taken_by = property()

    @taken_by.getter
    def taken_by(self):
        return self._taken_by

    @taken_by.setter
    def taken_by(self, pikcher_name):
        self._taken_by = pikcher_name

    def use_for_poll(self):
        self._use_for_poll = True

    def dont_use_for_poll(self):
        self._use_for_poll = False

    def to_dict(self):
        article_dict = dict()
        article_dict['link'] = self.link
        article_dict['kind'] = self.kind
        article_dict['rubrics'] = list(self.rubrics)
        article_dict['header'] = self.header
        article_dict['published'] = self.published.strftime('%Y-%m-%d %H:%M')

        if self.for_poll:
            article_dict['poll'] = self.for_poll
        if self.taken_by:
            article_dict['taken_by'] = self.taken_by

        return article_dict

    def __str__(self):
        return self.link