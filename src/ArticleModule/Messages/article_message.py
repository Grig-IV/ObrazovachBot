import math
import datetime as dt

from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from src.AbstractClasses.abstract_message import Message


class ArticleMessage(Message):
    MAX_ARTICLES_ON_PAGE = 6

    def __init__(self, pikcher, free_articles, last_update):
        curr_a_type = pikcher.data['currArticleTypeShow']
        db_message_id = str(pikcher.data['databaseMessageId'])
        pikcher_tz = dt.timezone(dt.timedelta(hours=pikcher.time_zone))
        if pikcher.data['rubricFilter']:
            rubric_filter = set(pikcher.data['rubricFilter'])
        else:
            rubric_filter = set()

        type_filter = lambda a: a.type == curr_a_type
        articles_of_type = list(filter(type_filter, free_articles))

        articles_count = len(articles_of_type)
        pagination_data = self._get_pagination_data(pikcher, articles_count)
        reply_markup = ArticleMessage.create_reply_markup(curr_a_type,
                                                          pagination_data,
                                                          db_message_id)

        curr_page, _ = pagination_data
        articles_on_page = self._get_articles_to_show(articles_of_type,
                                                      rubric_filter,
                                                      curr_page)

        text = self._get_message_text(articles_on_page,
                                      pikcher_tz,
                                      last_update)

        super().__init__(text, reply_markup=reply_markup)

    def _get_pagination_data(self, pikcher, articles_count):
        if articles_count == 0:
            total_pages = 1
        else:
            max_articals_on_page = ArticleMessage.MAX_ARTICLES_ON_PAGE
            total_pages = math.ceil(articles_count / max_articals_on_page)

        curr_page = pikcher.data['currentPage']
        if curr_page >= total_pages:
            curr_page = total_pages - 1

        return curr_page, total_pages

    def _get_articles_to_show(self, free_articles, rubric_filter, curr_page):
        max_a_on_page = ArticleMessage.MAX_ARTICLES_ON_PAGE

        f_func = lambda a: a.rubrics.intersection(rubric_filter) == set()
        articles = list(filter(f_func, free_articles))
        articles.sort(key=lambda a: a.published, reverse=True)
        articles_on_page = articles[curr_page * max_a_on_page:
                                    (curr_page + 1) * max_a_on_page]

        return articles_on_page

    def _get_message_text(self, articels_list, time_zone, last_update):
        heading_line = "<b>Список свободных статей:</b>\n\n"

        if last_update is not None:
            tz_last_update = last_update.replace(tzinfo=time_zone)
        else:
            tz_last_update = dt.datetime.now(tz=time_zone)
        srt_last_update = tz_last_update.strftime("%H:%M")
        date_line = "<i>Последний раз обновлено в " + srt_last_update + "</i>"

        if not articels_list:
            body = "<i>Свободных статей из этой темы не осталось</i>\n\n"
            return heading_line + body + date_line

        body = str()
        for article in articels_list:
            line = '<a href="{0}">{1}</a> | {2}\n\n'

            if article.is_for_poll:
                line = line.replace('|', '| *')

            published = self._get_publish_date_for_display(time_zone,
                                                           article.published)

            body += line.format(article.url, published, article.header)

        return heading_line + body + date_line

    def _get_publish_date_for_display(self, time_zone, publish_date):
        day_past = dt.datetime.now(time_zone).date() - publish_date.date()
        if day_past == dt.timedelta(days=0):
            published = "Сегодня"
        elif day_past == dt.timedelta(days=1):
            published = "Вчера"
        else:
            published = publish_date.strftime('%d.%m')

        return published

    def create_reply_markup(curr_a_type, pagination_data, db_message_id):
        button_lines = [
            ArticleMessage._get_article_type_line(curr_a_type, db_message_id),
            ArticleMessage._get_pagination_line(pagination_data, db_message_id),
            ArticleMessage._get_refresh_line(db_message_id)
        ]
        return InlineKeyboardMarkup(button_lines)

    def _get_article_type_line(curr_a_type, db_message_id):
        callback_data_temp = "switch_article_type {0} " + db_message_id

        text = "Новости" if curr_a_type != 'news' else "· Новости ·"
        callback_data = callback_data_temp.format('news')
        news_btn = InlineKeyboardButton(text, callback_data=callback_data)

        text = "Материалы" if curr_a_type != 'material' else "· Материалы ·"
        callback_data = callback_data_temp.format('material')
        material_btn = InlineKeyboardButton(text, callback_data=callback_data)

        text = "Блоги" if curr_a_type != 'blog' else "· Блоги ·"
        callback_data = callback_data_temp.format('blog')
        blog_btn = InlineKeyboardButton(text, callback_data=callback_data)

        articles_type_line = [news_btn, material_btn, blog_btn]

        return articles_type_line

    def _get_pagination_line(pagination_data, db_message_id):
        curr_page, total_pages = pagination_data
        callback_data_temp = 'switch_page {0} ' + db_message_id
        switch_buttons = list()
        for i in range(total_pages):
            clb_data = callback_data_temp.format(str(i))
            btn = InlineKeyboardButton(str(i + 1), callback_data=clb_data)
            switch_buttons.append(btn)

        switch_buttons[curr_page].text = '· {0} ·'.format(curr_page + 1)

        return switch_buttons

    def _get_refresh_line(db_message_id):
        text = "Обновить"
        callback_data = 'refresh None ' + db_message_id
        refresh_btn = InlineKeyboardButton(text, callback_data=callback_data)
        refresh_line = [refresh_btn]
        return refresh_line
