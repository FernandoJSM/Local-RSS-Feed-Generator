import utils
from scrapers.base_scraper import BaseScraper
import json
import rfeed
from datetime import datetime


class FeedGenerator:
    def __init__(self):
        self.scrapers = dict()

    def add_scraper(self, scraper_route, scraper: BaseScraper):
        self.scrapers[scraper_route] = scraper

    def create_feed(self, scraper_name):
        """
            Criar o Feed rss
        Args:
            scraper_name (str): Nome do scraper
        Returns:
            rss_feed (str): Arquivo xml do feed rss
        """
        scraper_obj = self.scrapers[scraper_name]
        with open(file=scraper_obj.db_path, mode="r", encoding="utf8") as db_file:
            stored_data = json.load(db_file)

        feed_items = list()

        for item in stored_data:
            feed_items.append(
                rfeed.Item(
                    title=item["title"],
                    link=item["link"],
                    description=None,
                    author=item["author"],
                    guid=rfeed.Guid(item["guid"]),
                    pubDate=datetime.fromtimestamp(item["publication_date"]),
                )
            )

        if scraper_obj.feed_info.image is not None:
            feed_image = rfeed.Image(
                url=scraper_obj.feed_info.image,
                title=scraper_obj.feed_info.title,
                link=scraper_obj.feed_info.link,
            )
        else:
            feed_image = None

        feed = rfeed.Feed(
            title=scraper_obj.feed_info.title,
            link=scraper_obj.feed_info.link,
            description=scraper_obj.feed_info.description,
            language=scraper_obj.feed_info.language,
            image=feed_image,
            lastBuildDate=datetime.now(),
            items=feed_items,
        )

        return feed.rss()


if __name__ == "__main__":
    from scrapers.marinha_scraper import MarinhaScraper
    from scrapers.feed_data import FeedInfo

    marinha_info = FeedInfo(
        title="Marinha do Brasil",
        link="https://www.marinha.mil.br",
        description="Notícias da Marinha do Brasil",
        language="pt-br",
        image="https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico",
    )

    feed_generator = FeedGenerator()
    feed_generator.add_scraper(
        scraper_route="marinha_news",
        scraper=MarinhaScraper(
            feed_info=marinha_info,
            database_path=utils.get_data_filepath(filename="marinha.json"),
            max_items=30,
        ),
    )

    rss_feed = feed_generator.create_feed(scraper_name="marinha_news")
    print(rss_feed)
