from abc import ABC, abstractmethod
from typing import List

from scrapers.feed_item import FeedItem


class BaseScraper(ABC):
    """
    Classe de base para os scrapers implementados no código
    """

    @abstractmethod
    def scrape_page(self) -> List[FeedItem]:
        """
        Coleta os dados da página e retorna uma lista com os itens do Feed RSS
        """
        pass
