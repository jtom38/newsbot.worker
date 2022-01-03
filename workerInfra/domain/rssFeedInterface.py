from abc import ABC, abstractclassmethod
from workerInfra.domain.loggerInterface import LoggerInterface
from workerInfra.models.dbModels import Articles
from bs4 import BeautifulSoup
from typing import Dict, List, Union


class RssFeedInterface(ABC):
    _logger: LoggerInterface
    _url: str
    _siteName: str
    _sourceId: str
    _soup: Union[BeautifulSoup, Dict]

    @abstractclassmethod
    def collectItems(self) -> List[BeautifulSoup]:
        """This collects all the items from the feed."""
        ...

    @abstractclassmethod
    def processItem(self, soup: BeautifulSoup) -> Articles:
        ...

    @abstractclassmethod
    def getTitle(self) -> str:
        ...

    @abstractclassmethod
    def getAuthorName(self) -> str:
        ...

    @abstractclassmethod
    def getPublishDate(self) -> str:
        ...

    @abstractclassmethod
    def getDescription(self) -> str:
        ...

    @abstractclassmethod
    def getThumbnail(self) -> str:
        ...

    @abstractclassmethod
    def getTags(self) -> str:
        """Searches the _soup object to find any tags by a defined list."""
        ...

    @abstractclassmethod
    def getLink(self) -> str:
        """Searches the _soup object to find the link object."""
        ...

    # @abstractclassmethod
    # def checkSiteIcon(self) -> None:
    #     raise NotImplementedError()

