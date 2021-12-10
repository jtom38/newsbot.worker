from abc import ABC, abstractclassmethod
from typing import List
from workerInfra.domain.loggerInterface import LoggerInterface
from workerInfra.enum import SourcesEnum, SourceTypeEnum
from workerInfra.models import Articles


class SourcesInterface(ABC):
    _logger: LoggerInterface
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
    def setSiteName(self, siteName: SourcesEnum) -> None:
        """
        This can be found on BaseSources
        """
        raise NotImplementedError

    def setSourceType(self, type: SourceTypeEnum) -> None:
        """
        This can be found on BaseSources
        """
        raise NotImplementedError()

    def setActiveSource(self, sourceName: SourcesEnum, type: SourceTypeEnum = SourceTypeEnum.INVALID) -> None:
        raise NotImplementedError()
