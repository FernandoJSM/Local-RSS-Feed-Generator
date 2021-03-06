import utils
from scrapers.base_scraper import BaseScraper
import logging
import requests
from bs4 import BeautifulSoup
from bs4 import element
from datetime import datetime
from scrapers.feed_data import FeedItem
import json
import dataclasses


class MarinhaScraper(BaseScraper):
    """
    Extrai informações da página de notícias da Marinha do Brasil
    """

    def __init__(
        self,
        feed_info,
        database_path,
        max_items,
        url="https://www.marinha.mil.br/todas-noticias",
    ):
        """
        feed_info (FeedInfo obj): Dados do feed
        database_path (str): Caminho do arquivo json do banco de dados
        max_items (int): Quantidade máxima de notícias armazenadas
        url (str): URL da página de notícias da Marinha do Brasil
        """
        self.feed_info = feed_info
        self.db_path = database_path
        self.max_items = max_items
        self.url = url
        self.session = None

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(message)s",
            level=logging.INFO,
            datefmt="%d-%m-%Y %H:%M:%S",
        )

        self.logger = logging.getLogger(name=feed_info.title)

    def get_news_list(self, page_number):
        """
            Acessa a página com a lista de notícias
        Args:
            Returns:
                webpage (requests obj): Objeto resultante da requisição
        """
        self.logger.info(msg=f"Acessando a página {page_number}...")
        webpage = self.session.get(url=self.url + f"?page={page_number}")

        if webpage.status_code != 200:
            self.logger.info(msg="Não foi possível acessar a página")
            return None

        self.logger.info(msg="Página acessada, obtendo os dados...")
        return webpage

    @staticmethod
    def extract_news(page_source):
        """
            Extrai as notícias da página
        Args:
            page_source (str): Código fonte da página
        Returns
            feed_items (List[FeedItem]): Lista com itens de feed rss criados a partir da leitura da página
        """
        soup = BeautifulSoup(markup=page_source, features="html.parser")
        feed_items = list()

        raw_news_list = soup.find_all(name="div", attrs={"class": "view-content"})[0]
        news_list = [
            tag for tag in list(raw_news_list.children) if isinstance(tag, element.Tag)
        ]

        for article in news_list:
            title = article.find_all(name="a")[0].text.strip()
            link = (
                "https://www.marinha.mil.br"
                + article.find_all(name="a")[0].attrs["href"]
            )

            author_find = article.find_all(
                name="div", attrs={"class": "views-field views-field-field-editoria"}
            )
            if author_find:
                author = author_find[0].text.strip()
            else:
                author = None

            date_string = article.find_all(
                name="div", attrs={"class": "field-content"}
            )[0].text.strip()
            publication_date = datetime.strptime(
                date_string + "-0300", "%d/%m/%Y - %H:%M%z"
            )

            feed_items.append(
                FeedItem(
                    title=title,
                    link=link,
                    description=title,
                    author=author,
                    guid=link,
                    publication_date=int(publication_date.timestamp()),
                )
            )

        return feed_items

    def scrape_page(self):
        """
            Acessa a página e extrai as notícias conforme a configuração
        Returns:
            feed_items (List[FeedItem]): Lista com itens de feed rss criados a partir da leitura da página
        """
        self.session = requests.session()

        webpage = self.get_news_list(page_number=1)
        if webpage is None:
            return list()

        colected_items = self.extract_news(page_source=webpage.text)
        current_page = 1

        while len(colected_items) < self.max_items:
            current_page += 1
            webpage = self.get_news_list(page_number=current_page)
            if webpage is None:
                break

            items_to_add = self.extract_news(page_source=webpage.text)

            total_colected = len(colected_items) + len(items_to_add)
            if total_colected > self.max_items:
                difference = total_colected - self.max_items
                colected_items.extend(items_to_add[:difference])
            else:
                colected_items.extend(items_to_add)

        output_data = [dataclasses.asdict(news) for news in colected_items]

        with open(file=self.db_path, mode="w", encoding="utf8") as db_file:
            json.dump(obj=output_data, fp=db_file, indent=4)


if __name__ == "__main__":
    from scrapers.feed_data import FeedInfo

    marinha_info = FeedInfo(
        title="Marinha do Brasil",
        link="https://www.marinha.mil.br",
        description="Notícias da Marinha do Brasil",
        language="pt-br",
        image="https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico",
    )
    scraper = MarinhaScraper(
        feed_info=marinha_info,
        database_path=utils.get_data_filepath(filename="marinha.json"),
        max_items=30,
    )

    scraper.scrape_page()
