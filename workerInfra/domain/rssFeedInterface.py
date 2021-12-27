from abc import ABC, abstractclassmethod
from typing import List


class RssFeedInterface(ABC):
    @abstractclassmethod
    def checkSiteIcon(self) -> None:
        raise NotImplementedError()

    @abstractclassmethod
    def getPosts(self) -> List:
        raise NotImplementedError()

    @abstractclassmethod
    def findFeedTitle(self) -> str:
        raise NotImplementedError()

    @abstractclassmethod
    def findItemLink(self) -> str:
        raise NotImplementedError()
