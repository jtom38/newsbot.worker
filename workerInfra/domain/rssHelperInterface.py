from abc import ABC, abstractclassmethod
from bs4 import BeautifulSoup
# from workerService import RequestArticleContent


class RssHelperInterface(ABC):
    """
    This interface is used to define how the RssReader can intagrate with sites witout a full source.
    """

    _soup: BeautifulSoup

    @abstractclassmethod
    def getArticleContent(self) -> str:
        """
        Checks the soup object and finds the content of the article.

        Returns: str
        """
        raise NotImplementedError

    def cacheSite(self, soup: BeautifulSoup):
        self.soup = soup
