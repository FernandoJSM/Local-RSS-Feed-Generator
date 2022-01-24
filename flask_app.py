from flask import Flask
import utils
from feed_generator import FeedGenerator
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

flask_app = Flask(import_name=__name__)


@flask_app.route("/<scraper_route>")
def get_feed(scraper_route):
    if scraper_route in feed_generator.scrapers:
        feed_generator.scrapers[scraper_route].scrape_page()
        rss_feed = feed_generator.create_feed(scraper_name=scraper_route)
        return rss_feed
    else:
        return "Feed não encontrado"


flask_app.run()
