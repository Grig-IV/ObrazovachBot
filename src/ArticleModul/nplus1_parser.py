import requests

from bs4 import BeautifulSoup

from src.models.article import Article


class NP1_Parser:
    def get_links_on_main(self):
        """
        Return all links on main page (without partner materials).
        """
        main_page = requests.get("https://nplus1.ru")
        main_html = BeautifulSoup(main_page.text, 'html.parser')

        # Articles parsing
        articles_tags_on_main = main_html.select("#main article")
        articles_tags_on_main = filter(
            # Ignor promo materials
            lambda t: 'Партнерский материал' not in str(t),
            articles_tags_on_main)
        articles_links = map(lambda t: t.a['href'], articles_tags_on_main)
    
        return articles_links
