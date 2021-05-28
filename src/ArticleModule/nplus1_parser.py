import requests

import aiohttp

from bs4 import BeautifulSoup


class Parser_NP1:
    MAIN_URL = "https://nplus1.ru"

    def get_links_on_main():
        """
        Return all links on main page (without partner materials).
        """
        main_page = requests.get(Parser_NP1.MAIN_URL)
        main_html = BeautifulSoup(main_page.text, 'html.parser')

        # Articles parsing
        articles_tags_on_main = main_html.select("#main article")
        articles_tags_on_main = filter(
            # Ignor promo materials
            lambda t: 'Партнерский материал' not in str(t),
            articles_tags_on_main)
        articles_links = map(lambda t: t.a['href'], articles_tags_on_main)

        return set(articles_links)

    async def load_page(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(Parser_NP1.MAIN_URL + link) as response:
                return await response.text()

    def parse_page(article_page):
        """
        Parse article date by link.
        """
        article_html = BeautifulSoup(article_page, 'html.parser')

        link_tag = article_html.select_one('meta[property="og:url"]')
        article_link = link_tag['content'].replace(Parser_NP1.MAIN_URL, "")

        rubrics_tags_table = article_html.select("p.table a[data-rubric]")
        if rubrics_tags_table:
            rubrics_list = map(lambda a: a['data-rubric'], rubrics_tags_table)
        else:
            rubrics_list = ['none']

        # YYYY-MM-DD
        pb_date = article_html.select_one("div.meta time")['content']
        # HH:MM
        pb_time = article_html.select_one("div.meta time > span").get_text()
        published_dt_str = pb_date + ' ' + pb_time

        article_header = article_html.select_one("header h1").get_text()
        article_type = article_link.split('/')[1]
        if article_type == "material":
            subtitle = article_html.select_one("p.subtitle").get_text()
            article_header = "{0} | {1}".format(article_header, subtitle)

        article_dict = {
            'link': article_link,
            'rubrics': set(rubrics_list),
            'header': article_header,
            'published_str': published_dt_str
        }

        return article_dict
