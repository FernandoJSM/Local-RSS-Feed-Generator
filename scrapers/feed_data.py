from dataclasses import dataclass


@dataclass
class FeedInfo:
    """
    Contém dados do feed RSS
    """

    title: str
    link: str
    description: str
    language: str
    image: str


@dataclass
class FeedItem:
    """
    Contém dados para item de um feed RSS
    """

    title: str
    link: str
    description: str
    author: str or None
    guid: str
    publication_date: int
