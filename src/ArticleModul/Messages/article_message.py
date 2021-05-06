from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from src.AbstractClasses.abstract_message import Message


class ArticleMessage(Message):
    MAX_ARTICLES_ON_PAGE = 6
    def __init__(self, pikcher, free_articles, last_update):
        curr_a_type = pikcher.data['currArticlesTypeShow']
        db_message_id = pikcher.data['databaseMessageId']
        rubric_filter = set(pikcher.date['rubricFilter'])
        curr_page = pikcher.date['currentPage']

        articles = list(filter(lambda a: a.type == curr_a_type,
                               free_articles))
        curr_page = self._curr_page_tuning(curr_page, len(articles))
        
        articles_on_page = self._get_articles_to_show(articles,
                                                      rubric_filter,
                                                      curr_page)
        self.text = self._get_message_text(articles_on_page,
                                      pikcher.time_zone,
                                      last_update)

        self.reply_markup = self._get_keyboard(pikcher, free_articles)

    def _curr_page_tuning(self, curr_page, numb_articles):
        if numb_articles == 0:
            numb_pages = 1
        else:
            max_articals_on_page = ArticleView.MAX_ARTICLES_ON_PAGE
            numb_pages = math.ceil(articles_numb / max_articals_on_page)

        if curr_page >= numb_pages:
            curr_page = numb_pages - 1

        return curr_page

    def _get_articles_to_show(self, free_articles, rubric_filter, curr_page):
        max_a_on_page = ArticleView.MAX_ARTICLES_ON_PAGE

        f_func = lambda a: a.rubrics.intersection(rubric_filter) is set()
        articles = list(filter(f_func, free_articles))
        articles.sort(key=lambda a: a.published, reverse=True)
        articles_on_page = articles[curr_page * max_a_on_page:
                                    (curr_page + 1) * max_a_on_page]

        return articles_on_page
        
    def _get_message_text(self, articels_list, time_zone, last_update):
        heading_line = "<b>Список свободных статей:</b>\n\n"

        tz_last_update = last_update.replace(tzinfo=time_zone)
        srt_last_update = tz_last_update.strftime("%H:%M")
        date_line = "<i>Последний раз обновлено в " + srt_last_update + "</i>"

        if not articels_list:
            body = "<i>Свободных статей из этой темы не осталось</i>\n\n"
            return heading_line + body + date_line

        body = str()
        for article in articels_list:
            line = '<a href="{0}">{1}</a> | {2}\n\n'

            if article.for_poll:
                line = line.replace('|', '| *')

            published = self._get_publish_date_for_display(article.published)

            body += line.format(article.url, published, article.header)

        return heading_line + body + date_line

    def _get_publish_date_for_display(self, publish_date):
        day_past = dt.datetime.now(self.tz).date() - publish_date
        if day_past == dt.timedelta(days=0):
            published = "Сегодня"
        elif day_past == dt.timedelta(days=1):
            published = "Вчера"
        else:
            published = publish_date.strftime('%m.%d')

        return published

    def _get_keyboard(self, curr_a_type, curr_page,
                      articles_numb, db_message_id):
        a_t_line = self._get_article_type_line(curr_a_type, db_message_id)
        p_n_line = self._get_page_numbs_line(articles_numb, db_message_id)
        r_line = self._get_refresh_line(db_message_id)

        button_lines = [a_t_line, p_n_line, r_line]
        keyboard = InlineKeyboardMarkup(button_lines)

        return keyboard

    def _get_article_type_line(self, curr_a_type, db_message_id):
        callback_data_temp = "switch_artcls_type {0} " + db_message_id

        text = "Новости" if curr_type != 'news' else "· Новости ·"
        callback_data = callback_data_temp.format('news')
        news_btn = InlineKeyboardButton(text, callback_data=callback_data)

        
        text = "Материалы" if curr_type != 'material' else "· Материалы ·"
        callback_data = callback_data_temp.format('material')
        material_btn = InlineKeyboardButton(text, callback_data=callback_data)
        
        text = "Блоги" if curr_type != 'blog' else "· Блоги ·"
        callback_data = callback_data_temp.format('blog')
        blog_btn = InlineKeyboardButton(text, callback_data=callback_data)

        articles_type_line = [news_btn, material_btn, blog_btn]

        return articles_type_line

    def _get_page_numbs_line(self, curr_page, articles_numb, db_message_id):
        max_articals_on_page = ArticleView.MAX_ARTICLES_ON_PAGE
        numb_pages = math.ceil(articles_numb / max_articals_on_page)

        callback_data_temp = 'switch_page {0} ' + db_message_id
        switch_buttons = list()
        for i in range(numb_pages):
            clb_data = callback_data_temp.format(str(i))
            btn = InlineKeyboardButton(str(i + 1), callback_data=clb_data)
            switch_buttons.append(btn)
        
        switch_buttons[curr_page].text = '· {0} ·'.format(curr_page + 1)

        return switch_buttons

    def _get_refresh_line(self):
        text = "Обновить"
        callback_data = 'refresh None ' + db_id
        refresh_btn = InlineKeyboardButton(text, callback_data=callback_data)
        refresh_line = [refresh_btn]
        return refresh_line
