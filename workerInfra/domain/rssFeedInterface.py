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
        """Process a single entry from the feed."""
        ...

    @abstractclassmethod
    def getTitle(self) -> str:
        """Gets the title from the stored soup object against known values."""
        ...

    @abstractclassmethod
    def getAuthorName(self) -> str:
        """Gets the author name from the stored soup object against known values."""
        ...

    @abstractclassmethod
    def getPublishDate(self) -> str:
        """Gets the publish date from the stored soup object against known values."""
        ...

    @abstractclassmethod
    def getDescription(self) -> str:
        """Gets the description/content from the stored soup object against known values."""
        ...

    @abstractclassmethod
    def getThumbnail(self) -> str:
        """Gets the thumbnail from the stored soup object against known values."""
        ...

    @abstractclassmethod
    def getTags(self) -> str:
        """Searches the _soup object to find any tags by a defined list."""
        ...

    @abstractclassmethod
    def getLink(self) -> str:
        """Searches the _soup object to find the link object."""
        ...
