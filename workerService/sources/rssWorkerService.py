from typing import List, Dict
import re
from bs4 import BeautifulSoup
from json import loads
from workerInfra.domain import LoggerInterface, SourcesInterface, DriverInterface, CacheInterface
from workerInfra.domain.rssFeedInterface import RssFeedInterface
from workerInfra.enum import SourcesEnum
from workerInfra.base import SourcesBase
from workerInfra.models import Articles, Icons
from workerService.logger import BasicLoggerService
from workerService.db import ArticlesTable, IconsTable
from workerService import RequestSiteContent, RequestArticleContent, RequestContent, CacheFactory, SqlCache
from workerService.sources.rssHelperService import *


class RssWorkerService(SourcesBase, SourcesInterface):
    _logger: LoggerInterface
    _driver: DriverInterface
    _cache: CacheInterface
    _parser: RssFeedInterface
    _helper: RssHelperInterface
    _feedName: str
    _uri: str

    def __init__(self) -> None:
        self._logger = BasicLoggerService()
        self._cache = CacheFactory(SqlCache())
        self.uri = "https://example.net/"
        self.setSiteName(SourcesEnum.RSS)
        self.setActiveSource(SourcesEnum.RSS)
        self.feedName: str = ""
        # self.RssHelper: IRssContent = IRssContent()

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for link in self.__links__:
            # link: Sources = link

            if link.enabled is False:
                continue

            self._logger.debug(f"{link.source} - {link.name} - Checking for updates")
            self.setActiveSource(source=SourcesEnum.RSS, name=link.name)
            self.feedName = link.name

            # Cache the root site
            self.uri = link.url
            if 'http://' in self.uri or 'https://' in self.uri:
                pass
            else:
                self._logger.warning(f"Found a invalid url in the database. Name: {link.name} - Url: {link.url}.  It should be updated.  Skipping over it for now.")
                continue
            
            rsc = RequestSiteContent(url=link.url)
            rsc.getPageDetails()

            # Check if the site icon has been cached
            iconsExists = IconsTable().getBySite(site=link.name)
            if iconsExists.id == '':
                siteIcon: str = rsc.findSiteIcon(link.url)
                IconsTable().update(Icons(filename=siteIcon, site=link.name))

            # Check if we have helper code for deeper RSS integration
            # hasHelper: bool = self.enableHelper(link.url)

            # Determin what typ of feed is on the site
            feed = rsc.findFeedLink(siteUrl=link.url)
            if feed["type"] == "atom":
                ap = AtomParser(url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())
                items = ap.getPosts()
                for i in items:
                    a: Articles = ap.parseItem(i)
                    if a.title != "":
                        self._logger.debug(f"Collected item '{a.title} from {link.name}")
                        allArticles.append(a)

            elif feed["type"] == "rss" or feed['type'] == "feedburner":
                rp = RssParser(url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())
                items = rp.getPosts()
                for item in items:
                    a = rp.processItem(item=item, title=link.name)
                    if a.title != "":
                        self._logger.debug(f"Collected item '{a.title} from {link.name}")
                        allArticles.append(a)

            elif feed["type"] == "json":
                jp = JsonParser(url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())
                items = jp.getPosts()
                for i in items:
                    a: Articles = jp.parseItem(i)
                    if a.title != "":
                        self._logger.debug(f"Collected item '{a.title} from {link.name}")
                        allArticles.append(a)

            else:
                # Unable to find a feed in the page's source code.
                rp = RssParser(url=link.url, siteName=link.name)
                items = rp.getPosts()
                if len(items) >= 1:
                    for item in items:
                        a = rp.processItem(item=item, title=link.name)
                        if a.title != "":
                            self._logger.debug(f"Collected item '{a.title} from {link.name}")
                            allArticles.append(a)
                else:
                    self._logger.error(
                        f"Unable to find a feed for '{link.name}'.  This source is getting disabled."
                    )
                    for linkDiff in self.__links__:
                        #link: Sources = link
                        if link.name == linkDiff.name:
                            linkDiff.enabled = False

        return allArticles

    def enableHelper(self, url: str) -> bool:
        r: bool = False
        if "engadget.com" in url:
            # self.RssHelper = Engadget()
            self._helper = Engadget()
            r = True
        elif "arstechnica" in url:
            self._helper = ArsTechnica()
            r = True
        elif "howtogeek" in url:
            self._helper = HowToGeek()
            r = True
        return r


class AtomParser(RssFeedInterface):
    def __init__(self, url: str, siteName: str, sourceId: str) -> None:
        self.url: str = url
        self.siteName: str = siteName
        self.content = RequestSiteContent(url=url)
        self.content.getPageDetails()
        self.sourceId: str = sourceId
        pass

    def findFeedTitle(self) -> str:
        title = self.content.findSingle(name="title")
        return title

    def getPosts(self) -> List:
        return self.content.findMany(name="entry")

    def getTitle(self) -> str:
        return self.__item__.find(name="title").text.replace("\n", "").strip()

    def getPublishDate(self) -> str:
        return self.__item__.find(name="updated").text

    def getAuthorName(self) -> str:
        author = self.__item__.find(name="author")
        if "github.com" in self.url:
            return author.find(name="name").text
        else:
            return author.text

    def getDescription(self) -> str:
        text: str = self.__item__.find(name="content").text

        # this works on github commits
        if ">" in text and "<" in text:
            text = re.findall(">(.*?)<", text)[0]
        return text

    def getThumbnail(self) -> str:
        rc = RequestContent(url=self.url)
        rc.getPageDetails()
        return rc.findArticleThumbnail()

    def parseItem(self, item: BeautifulSoup) -> Articles:
        self.__item__: BeautifulSoup = item
        # feedTitle: str = self.content.findSingle(name="title")

        url = item.find(name="link", attrs={"type": "text/html"}).attrs["href"]
        exists = ArticlesTable().getByUrl(url)
        if exists.id == '':
            a = Articles(
                sourceId=self.sourceId,
                tags=f"RSS, {self.siteName}",
                title=self.getTitle(),
                pubDate=self.getPublishDate(),
                url=url,
                authorName=self.getAuthorName(),
                description=self.getDescription(),
                thumbnail=self.getThumbnail()
            )

        return a


class RssParser(RssFeedInterface):
    _logger: LoggerInterface

    def __init__(self, url: str, siteName: str, sourceId: str) -> None:
        self._logger = BasicLoggerService()
        self.url: str = url
        self.siteName: str = siteName
        self.content: RequestSiteContent = RequestContent(url=url)
        self.content.getPageDetails()
        self.sourceId: str = sourceId
        # self.rssHelper: IRssContent = rssHelper
        pass

    def checkSiteIcon(self) -> None:
        pass

    def findFeedTitle(self) -> str:
        pass

    def getPosts(self) -> List:
        return self.content.findMany(name="item")

    def processItem(self, item: BeautifulSoup, title: str) -> Articles:
        # get the link for the article
        url = self.findItemLink(item)
        if url == "" or url is None or url == "https://":

            # did not find a valid url, pass back a blank object
            return Articles()

        # Check if we have already looked atthis link
        exists = ArticlesTable().getByUrl(url=url)
        if exists.id == "":
            # Set the new URI and store the source for now to avoid extra calls
            # rc = RequestContent(url=url)
            ra = RequestArticleContent(url=url)
            ra.getPageDetails()
            thumb = ra.findArticleThumbnail()

            description = ""
            # description = ra.findArticleDescription()

            a = Articles(
                title=item.find(name="title").text,
                description=self.findItemDescription(item, description),
                tags=self.findItemTags(item),
                url=url,
                pubDate=item.find(name="pubdate").text,
                authorName=self.findItemAuthor(item),
                sourceId=self.sourceId
            )
            a.thumbnail = thumb
        else:
            return Articles()
        return a

    def findItemDescription(self, item: BeautifulSoup, desc: str) -> str:
        i: str = ""
        if desc != "":
            return desc
        else:
            items = ("description", "content:encoded")
            for i in items:
                try:
                    # i:str = item.find(name="description").text
                    i = item.find(name=i).text
                    if i != "":
                        return i
                except Exception as e:
                    self._logger.warning(f"Unable to find the description of the post with the known items. {e}")
                    pass

            if i == "":
                self._logger.critical(
                    f"Failed to locate RSS body.  Review {self.url} for the reason"
                )
            return ""

    def findItemLink(self, item: BeautifulSoup) -> str:
        url: str = item.find(name="link").next
        url = url.replace("\n", "")
        url = url.replace("\t", "")
        url = url.replace("\r", "")
        url = url.strip()
        return url

    def findItemTags(self, item: BeautifulSoup) -> str:
        tags: List[str] = list()
        for i in item.find_all(name="category"):
            # lets vsc see the expected class
            i: BeautifulSoup = i
            tags.append(i.text)

        s = str(tags)
        return s

    def findItemAuthor(self, item: BeautifulSoup) -> str:
        items = ("author", "dc:creator")
        itemAuthor: str = ""
        for i in items:
            try:
                itemAuthor = item.find(name=i).text
                if itemAuthor != "":
                    return itemAuthor
            except Exception as e:
                pass
        if itemAuthor == '':
                self._logger.warning(f"Was unable to find the author on the RSS feed against the known items. {e}")
        return itemAuthor


class JsonParser(RssFeedInterface):
    def __init__(self, url: str, siteName: str, sourceId: str):
        self.url: str = url
        self.siteName: str = siteName
        self.rc = RequestArticleContent(url=url)
        self.rc.getPageDetails()
        self.json = loads(self.rc.__source__)
        self.sourceId: str = sourceId
        # self.articles = articlesTable

    def getPosts(self) -> List:
        return self.json["items"]

    def parseItem(self, item: Dict) -> Articles:
        exists = ArticlesTable().getByUrl(url=item["url"])
        if exists.id == '':
            rc = RequestContent(url=item["url"])
            rc.getPageDetails()
            a = Articles(
                tags=f"RSS, {self.siteName}",
                title=item["title"],
                url=item["url"],
                pubDate=item["date_published"],
                thumbnail=rc.findArticleThumbnail(),
                authorName=item["author"]["name"],
                description=item["content_html"],
                sourceId=self.sourceId
            )
        return a
