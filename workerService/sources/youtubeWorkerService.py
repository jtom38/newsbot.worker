from typing import List
from bs4 import BeautifulSoup
from workerInfra.domain.driverInterface import DriverInterface
from workerInfra.domain.loggerInterface import LoggerInterface
from workerInfra.models import Articles, Sources
from workerInfra.enum import SourcesEnum
from workerInfra.domain import SourcesInterface
from workerInfra.base import SourcesBase
from workerService import FirefoxDriverService
from workerService.logger import BasicLoggerService
from workerService.cache import Cache


class YoutubeWorkerService(SourcesBase, SourcesInterface):
    _logger: LoggerInterface
    _driver: DriverInterface

    def __init__(self):
        self._logger: LoggerInterface = BasicLoggerService()
        self.cache = Cache()
        self._driver: DriverInterface = FirefoxDriverService(self._logger)

        self.uri: str = "https://youtube.com"
        self.setSiteName(SourcesEnum.YOUTUBE)
        self.settingDebugScreenshots: bool = bool(self.cache.findBool(key='youtube.debug.screnshots'))
        self.feedBase: str = "https://www.youtube.com/feeds/videos.xml?channel_id="
        pass

    def getArticles(self) -> List[Articles]:
        self._logger.info("Checking YouTube for new content")

        allArticles: List[Articles] = list()

        for site in self.__links__:
            self.setActiveSource(source=SourcesEnum.YOUTUBE, name=site.name)
            self.authorName = ""
            self.authorImage = ""
            self._logger.debug(f"{site.source} - {site.name} - Checking for updates")

            # pull the source code from the main youtube page
            channelID = self.cache.find(key=f"{site.source}.{site.name}.channelID")
            if channelID == "":
                # self._driverSession = self._driver.driverStart()
                self._driver.start()
                self._driver.goTo(site.url)
                if self.settingDebugScreenshots is True:
                    self._driver.saveScreenshot(f"youtube_step1_{site.name}.png")

                siteContent: str = self._driver.getContent()
                page: BeautifulSoup = self.getParser(seleniumContent=siteContent)
                channelID: str = self.getChannelId(page)
                self.cache.add(key=f"youtube.{site.name}.channelID", value=channelID)

                # Not finding the values I want with just request.  Time for Chrome.
                # We are collecting info that is not present in the RSS feed.
                # We are going to store them in the class.
                self.setAuthorImage(page, site)
                self.setAuthorName(page, site)
                self._driver.close()
            else:
                self.authorName = self.cache.find(key=f"youtube.{site.name}.authorName")
                self.authorImage = self.cache.find(key=f"youtube{site.name}.authorImage")

            # Generatet he hidden RSS feed uri
            self.uri = f"{self.feedBase}{channelID}"
            siteContent = self.getContent()
            page = self.getParser(siteContent)

            root = page.contents[2].contents
            for item in root:
                if item.name == "entry":
                    a = Articles()
                    a.url = item.contents[9].attrs["href"]
                    a.video = a.url
                    a.title = item.contents[7].text
                    a.pubDate = item.contents[13].text
                    a.thumbnail = item.contents[17].contents[5].attrs["url"]
                    a.authorImage = self.authorImage
                    a.authorName = self.authorName
                    a.sourceId = self.getActiveSourceID()

                    allArticles.append(a)
        return allArticles

    def getChannelId(self, page: BeautifulSoup) -> str:
        meta = page.find_all("meta")
        for i in meta:
            try:
                if i.attrs["itemprop"] == "channelId":
                    channelId = i.attrs["content"]
                    return channelId
            except Exception as e:
                self._logger.error(f"Unable to find the ChannelId on the page.  Did the UI change? Error: {e}")
                pass

        return ""

    def setAuthorName(self, page: BeautifulSoup, site: Sources):
        try:
            authorName = page.find_all(
                name="yt-formatted-string",
                attrs={"class": "style-scope ytd-channel-name", "id": "text"},
            )
            self.authorName = authorName[0].text
            if self.authorName is None or self.authorName == '':
                self._logger.error(f"Failed to find the authorName for {site.name}.  CSS might have changed.")
            self.cache.add(
                key=f"youtube.{site.name}.authorName", value=self.authorName
            )
        except Exception as e:
            self._logger.error(
                f"Failed to find the authorName for {site.name}.  CSS might have changed. {e}"
            )

    def setAuthorImage(self, page: BeautifulSoup, site: Sources) -> str:
        try:
            authorImage = page.find_all(name="yt-img-shadow", attrs={"id": "avatar"})
            img = authorImage[0].contents[1].attrs["src"]
            if img != '':
                self.cache.add(
                    key=f"{site.source}.{site.name}.authorImage",
                    value=img,
                )
                self.authorImage = img
            else:
                self._logger.error("Failed to find the AuthorImage on the youtube page.")
        except Exception as e:
            self._logger.error(
                f"Failed to find the authorImage for {site.name}.  CSS might have changed. {e}"
            )
