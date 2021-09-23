from abc import ABC, abstractclassmethod
from typing import List
from newsbot.core.constant import SourceName, SourceType
from newsbot.core.sql import Articles


class ISources(ABC):
    uri: str = ''
    isSourceEnabled: bool = False
    isOutputDiscordEnabled: bool = False

    @abstractclassmethod
    def getArticles(self) -> List[Articles]:
        """
        This is the primary loop that checks the source to extract all the articles.
        """
        raise NotImplementedError

    @abstractclassmethod
    def __enableSource__(self) -> None:
        """
        This can be found on BaseSources
        """
        raise NotImplementedError

    @abstractclassmethod
    def setSiteName(self, siteName: SourceName) -> None:
        """
        This can be found on BaseSources
        """
        raise NotImplementedError

    def setSourceType(self, type: SourceType) -> None:
        """
        This can be found on BaseSources
        """
        raise NotImplementedError()

    def setActiveSource(self, sourceName: SourceName, type: SourceType = SourceType.INVALID) -> None:
        raise NotImplementedError()
