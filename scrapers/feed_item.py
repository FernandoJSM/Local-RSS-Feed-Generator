from dataclasses import dataclass


@dataclass
class FeedItem:
    """
    Contém dados para item de um feed RSS
    """
    title: str
    link: str
    image: str or None
    description: str
    author: str or None
    guid: str
    publication_date: int
