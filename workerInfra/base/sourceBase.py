from workerInfra.exceptions import MissingSourceID
from workerInfra.models import Sources, DiscordWebHooks, SourceLinks
from workerInfra.enum import SourcesEnum
from workerInfra.domain import LoggerInterface
from workerService.db import SourcesTable, ArticlesTable, SourceLinksTable, DiscordWebHooksTable
from workerService import CacheFactory, SqlCache
from workerService.logger import BasicLoggerService
from typing import List
from requests import Response, get
from bs4 import BeautifulSoup


class SourceValidator():
    """
    This class validates the variables configured for the source to ensure that things are in place as expected.
    """
    _logger: LoggerInterface

    def __startValidation__(self) -> None:
        self.__validateSiteName__()
        self.__validateUri__()
        pass

    def __validateSiteName__(self) -> None:
        if self.siteName == '':
            raise Exception("'siteName' is missing from the source.")

    def __validateUri__(self) -> None:
        if self.uri == "":
            raise Exception("'uri' is missing from the source.")

    def __checkEnv__(self, siteName: str) -> None:
        # Check if site was requested.
        discordServers = self.__isDiscordEnabled__(siteName)
        if len(discordServers) >= 1:
            self.isOutputDiscordEnabled = True
            self.__hooks__ = discordServers

        sources = self.__getSourceList__(siteName)
        if len(sources) >= 1:
            self.isSourceEnabled = True
            self.__links__ = sources

    def __getSourceList__(self, siteName: str) -> List[Sources]:
        _list = list()
        res = SourcesTable().getAllBySource(source=siteName)
        for i in res:
            _list.append(i)
        return _list

    def __isDiscordEnabled__(self, siteName: str) -> List[DiscordWebHooks]:
        h: List[DiscordWebHooks] = list()

        s = SourcesTable().getAllBySource(source=siteName)
        for i in s:
            sl: SourceLinks = SourceLinksTable().getBySourceId(i.id)
            if sl.id == '':
                # self._logger.warning(message=f"Went looking for a source record on {siteName}, but id was missing.")
                pass

            elif sl.discordID != "" or sl.discordID is not None:
                discordRef = DiscordWebHooksTable().getById(id=sl.discordID)
                if discordRef.enabled is True:
                    h.append(discordRef)
            else:
                continue
        return h


class SourcesBase(SourceValidator):
    """
    This class contains some common code found in the sources.  Do not use this on its own!
    """
    isOutputDiscordEnabled: bool = False
    isSourceEnabled: bool = False
    __hooks__: List[DiscordWebHooks] = list()
    __links__: List[Sources] = list()

    def __init__(self) -> None:
        self._logger: LoggerInterface = BasicLoggerService()
        self.__enableSource__()
        pass

    def __enableSource__(self) -> None:
        self.__startValidation__()
        self.__enableTables__()
        self.__checkEnv__(self.siteName)

    def __enableTables__(self) -> None:
        self.articlesTable = ArticlesTable()
        self.tableSources = SourcesTable()
        self.cache: CacheFactory = CacheFactory(SqlCache())

    def setSiteName(self, siteName: SourcesEnum) -> None:
        self.siteName = siteName.value

    def setActiveSource(self, source: SourcesEnum, name: str = "", sourceType: str = '') -> None:
        """
        This goes out and pulls the record to bind the article against the source.
        """
        if sourceType != '':
            res = SourcesTable().getByNameSourceType(name=name, source=source.value, type=sourceType)
            # raise Exception("Feature is not ready yet.")

        elif name != "":
            res: Sources = SourcesTable().getByNameAndSource(name=name, source=source.value)

        else:
            res: Sources = SourcesTable().getBySource(source.value)
        # res: Sources = SourcesTable().getBySource(source.value)
        if res.id == '':
            raise Exception("Requested source was not found.")

        self.__activeRecord__: Sources = res

    def getActiveSourceID(self) -> str:
        return self.__activeRecord__.id

    def getContent(self, uri: str = '') -> Response:
        try:
            headers = self.getHeaders()
            if uri == "":
                return get(self.uri, headers=headers)
            else:
                return get(url=uri, headers=headers)
        except Exception as e:
            self._logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(
        self, requestsContent: Response = "", seleniumContent: str = ""
    ) -> BeautifulSoup:
        try:
            if seleniumContent != "":
                return BeautifulSoup(seleniumContent, features="html.parser")
            else:
                return BeautifulSoup(requestsContent.content, features="html.parser")
        except Exception as e:
            self._logger.critical(f"failed to parse data returned from requests. {e}")

    def getHeaders(self) -> dict:
        # return {"User-Agent": "NewsBot - Automated News Delivery"}
        return {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/91.3"}
