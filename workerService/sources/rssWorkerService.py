from typing import List, Dict
import re
from bs4 import BeautifulSoup
from json import loads
from workerInfra.domain import LoggerInterface, SourcesInterface, DriverInterface, CacheInterface, RssHelperInterface
from workerInfra.domain.rssFeedInterface import RssFeedInterface
from workerInfra.enum import SourcesEnum
from workerInfra.base import SourcesBase
from workerInfra.models import Articles, Icons
from workerService.logger import BasicLoggerService
from workerService.db import ArticlesTable, IconsTable
from workerService import RequestSiteContent, RequestArticleContent, RequestContent, CacheFactory, SqlCache
from workerService.sources.rssHelperService import Engadget, HowToGeek, ArsTechnica


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
            if iconsExists.filename == '':
                siteIcon: str = rsc.findSiteIcon(link.url)
                IconsTable().update(Icons(filename=siteIcon, site=link.name))

            # Check if we have helper code for deeper RSS integration
            # hasHelper: bool = self.enableHelper(link.url)

            # Determin what typ of feed is on the site
            #if 'github' in link.url:
            #    self._parser = GitHubParser(_logger = self._logger, url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())

            feed = rsc.findFeedLink(siteUrl=link.url)
            if feed["type"] == "atom":
                self._parser = SoupParser(_logger = self._logger, url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())

            elif feed["type"] == "rss" or feed['type'] == "feedburner":
                self._parser = SoupParser(_logger = self._logger, url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())

            elif feed["type"] == "json":
                self._parser = JsonParser(_logger = self._logger, url=feed["content"], siteName=link.name, sourceId=self.getActiveSourceID())

            else:
                # Unable to find a feed in the page's source code.
                self._parser = SoupParser(_logger = self._logger, url=link.url, siteName=link.name, sourceId=self.getActiveSourceID())

            items = self._parser.collectItems()
            for item in items:
                a = self._parser.processItem(item=item)
                if a.title != "":
                    self._logger.debug(f"Collected item '{a.title}' from {link.name}")
                    allArticles.append(a)

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


class SoupParser(RssFeedInterface):
    """This parser is made to handle soup based objects.  
    RSS, Feedburner and atom are all converted to soup objects and parsed."""

    _logger: LoggerInterface
    _soup: BeautifulSoup
    _url: str
    _siteName: str
    _sourceId: str

    _knownRootKeys: List[str] = ('entry', 'item')
    _knownTitleKeys: List[str] = ('title', 'summary')
    _knownTagsKeys: List[str] = ('category', '')
    _knownAuthorKeys: List[str] = ('author', 'creator', 'dc:creator')
    _knownPublishDateKeys: List[str] = ("updated", "pubDate", 'pubdate')
    _knownDescriptionKeys: List[str] = ('content', 'content:encoded')
    _knownLinkKeys: List[str] = ('link')

    def __init__(self, _logger: LoggerInterface, url: str, siteName: str, sourceId: str) -> None:
        self._logger = _logger
        self._url: str = url
        self._siteName: str = siteName
        self.content = RequestSiteContent(url=url)
        self.content.getPageDetails()
        self._sourceId: str = sourceId
        pass

    def collectItems(self) -> List[BeautifulSoup]:
        items = list()
        for i in self._knownRootKeys:
            res = self.content.findMany(name=i)
            if len(res) >= 1:
                items.extend(res)
                return items
        #return self.content.findMany(name="entry")

    def processItem(self, item: BeautifulSoup) -> Articles:
        self._soup = item

        url = self.getLink()
        exists = ArticlesTable().getByUrl(url)
        if exists.id == '' and url != '':
            tags = self.getTags()
            a = Articles(
                sourceId=self._sourceId,
                tags=f"RSS, {self._siteName} {tags}",
                title=self.getTitle(),
                pubDate=self.getPublishDate(),
                url=url,
                authorName=self.getAuthorName(),
                description=self.getDescription(),
                thumbnail=self.getThumbnail(url)
            )

            return a
        else:
            return Articles()

    def getTitle(self) -> str:
        res: str = ''
        try:
            title = self._soup.find(name='title').text
            #summary = self.content.findSingle(name="summary")
            #summarySplit = summary.contents[0].split('=')
            res = title
        except Exception as e:
            pass

        if title == '':
            self._logger.warning("")

        return res

    def __getValue__(self, keys: List[str], lookingFor: str) -> str:
        res: str = ''
        for item in keys:
            if res != '':
                continue

            try:
                r = self._soup.find(name=item).text
                res = r
            except Exception as e:
                pass

        if res == '':
            self._logger.warning(f"Unable to find {lookingFor} against the feed for {self._siteName}.  Please review.")

        return res

    def __getValues__(self, keys: List[str], lookingFor: str) -> str:
        res: str = ''
        for item in keys:
            if res != '':
                continue

            try:
                r = self._soup.find_all(name=item)
                for i in r:
                    res += f", {i.text}"
            except Exception as e:
                pass

        if res == '':
            self._logger.warning(f"Unable to find {lookingFor} against the feed for {self._siteName}.  Please review.")

        return res

    def getAuthorName(self) -> str:
        return self.__getValue__(self._knownAuthorKeys, "Author Name")

    def getPublishDate(self) -> str:
        return self.__getValue__(self._knownPublishDateKeys, "Published Date")

    def getDescription(self) -> str:
        return self.__getValue__(self._knownDescriptionKeys, "description")

    def getThumbnail(self, url: str) -> str:
        rc = RequestContent(url=url)
        rc.getPageDetails()
        return rc.findArticleThumbnail()

    def getTags(self) -> str:
        return self.__getValues__(self._knownTagsKeys, "Tags")

    def getLink(self) -> str:
        res: str = ''
        url: BeautifulSoup = self._soup.find(name="link")

        try:
            if url.text != '':
                res = url.text
            if 'http' in url.next:
                res = url.next
            elif url.attrs['href'] != '':
                res = url.attrs['href']
        except Exception as e:
            self._logger.error(f"Unable to find the link to the article from {self._siteName}.  Please review the feed.")

        res = res.replace("\n", "")
        res = res.replace("\t", "")
        res = res.replace("\r", "")
        res = res.strip()
        return res


class GitHubParser(SoupParser):
    def getAuthorName(self) -> str:
        author: str = ''
        for lookup in self._knownTagsKeys:
            if author != "":
                continue

            try:
                author = self._soup.find(name=lookup).text
                if "github.com" in self.url:
                    return author.find(name="name").text
            except Exception as e:
                pass

        return author


class AtomParser(RssFeedInterface):
    _logger: LoggerInterface
    _soup: BeautifulSoup
    _url: str
    _siteName: str
    _sourceId: str

    def __init__(self, _logger: LoggerInterface, url: str, siteName: str, sourceId: str) -> None:
        self._logger = _logger
        self._url: str = url
        self._siteName: str = siteName
        self.content = RequestSiteContent(url=url)
        self.content.getPageDetails()
        self._sourceId: str = sourceId
        pass

    def collectItems(self) -> List[BeautifulSoup]:
        return self.content.findMany(name="entry")

    def processItem(self, item: BeautifulSoup) -> Articles:
        self._soup = item

        url = self.getLink()
        exists = ArticlesTable().getByUrl(url)
        if exists.id == '' and url != '':
            a = Articles(
                sourceId=self._sourceId,
                tags=f"RSS, {self._siteName}",
                title=self.getTitle(),
                pubDate=self.getPublishDate(),
                url=url,
                authorName=self.getAuthorName(),
                description=self.getDescription(),
                thumbnail=self.getThumbnail(url)
            )

        return a

    def getTitle(self) -> str:
        res: str = ''
        try:
            title = self.content.findSingle(name="title").text
            summary = self.content.findSingle(name="summary")
            summarySplit = summary.contents[0].split('=')
            res = title
        except Exception as e:
            pass

        if title == '':
            self._logger.warning("")

        return res

    def getAuthorName(self) -> str:
        lookups: List[str] = ('author', 'creator')
        author: str = ''
        for lookup in lookups:
            if author != "":
                continue

            try:
                author = self._soup.find(name=lookup).text
                if "github.com" in self.url:
                    return author.find(name="name").text
            except Exception as e:
                pass

        return author

    def getPublishDate(self) -> str:
        lookups: List[str] = ("updated", "pubDate")
        res: str = ''
        for lookup in lookups:
            if res != '':
                continue

            try:
                r = self._soup.find(name=lookup).text
                res = r
            except Exception as e:
                pass

        if res == '':
            self._logger.warning(f"Unable to find publish date against the feed for {self.siteName}.  Please review.")

        return res

    def getDescription(self) -> str:
        res: str = ''
        try:
            text: str = self._soup.find(name="content").text

            # this works on github commits
            if ">" in text and "<" in text:
                res = re.findall(">(.*?)<", text)[0]
        except Exception as e:
            pass

        return res

    def getThumbnail(self, url: str) -> str:
        rc = RequestContent(url=url)
        rc.getPageDetails()
        return rc.findArticleThumbnail()

    def getTags(self) -> str:
        lookups: List[str] = ("category")
        res: str = ''
        for lookup in lookups:
            if res != '':
                continue

            res = self._soup.find_all(name=lookup).text

        if res == '':
            self._logger.warning(f"Unable to find publish date against the feed for {self.siteName}.  Please review.")

        return res

    def getLink(self) -> str:
        res: str = ''
        url: BeautifulSoup = self._soup.find(name="link")

        try:
            if url.text != '':
                res = url.text
            elif url.attrs['href'] != '':
                res = url.attrs['href']
        except Exception as e:
            self._logger.error(f"Unable to find the link to the article from {self._siteName}.  Please review the feed.")

        res = res.replace("\n", "")
        res = res.replace("\t", "")
        res = res.replace("\r", "")
        res = res.strip()
        return res


class RssParser(SoupParser):
    _url: str
    _siteName: str
    _sourceId: str
    _logger: LoggerInterface
    _soup: BeautifulSoup

    def __init__(self, _logger: LoggerInterface, url: str, siteName: str, sourceId: str) -> None:
        self._logger = _logger
        self._url: str = url
        self._siteName: str = siteName
        self.content: RequestSiteContent = RequestContent(url=url)
        self.content.getPageDetails()
        self._sourceId: str = sourceId

    def collectItems(self) -> List:
        return self.content.findMany(name="item")

    def processItem(self, item: BeautifulSoup) -> Articles:
        self._soup = item
        # get the link for the article
        url = self.getLink()
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

            a = Articles(
                title=self.getTitle(),
                description=self.getDescription(),
                tags=self.getTags(),
                url=self.getLink(),
                pubDate=self.getPublishDate(),
                authorName=self.getAuthorName(),
                sourceId=self._sourceId
            )
            a.thumbnail = thumb
        else:
            return Articles()
        return a

    def getTitle(self) -> str:
        res = self._soup.find(name="title").text
        if res == '':
            self._logger.warning("Unable to find the title.")
        return res

    def getAuthorName(self) -> str:
        items = ("author", "dc:creator")
        itemAuthor: str = ""
        for i in items:
            try:
                itemAuthor = self._soup.find(name=i).text
                if itemAuthor != "":
                    return itemAuthor
            except Exception as e:
                self._logger.warning(e)
                pass
        if itemAuthor == '':
            self._logger.warning("Was unable to find the author on the RSS feed against the known items.")
        return itemAuthor

    def getPublishDate(self) -> str:
        res = self._soup.find(name="pubdate").text
        if res == '':
            self._logger.warning("Unable to find Publish Date.  Please review the source.")
        return res

    # def getDescription(self) -> str:
    #     i: str = ""
    #     if desc != "":
    #         return desc
    #     else:
    #         items = ("description", "content:encoded")
    #         for i in items:
    #             try:
    #                 # i:str = item.find(name="description").text
    #                 i = item.find(name=i).text
    #                 if i != "":
    #                     return i
    #             except Exception as e:
    #                 self._logger.warning(f"Unable to find the description of the post with the known items. {e}")
    #                 pass
 # 
    #         if i == "":
    #             self._logger.critical(
    #                 f"Failed to locate RSS body.  Review {self.url} for the reason"
    #             )
    #         return ""

    def getThumbnail(self) -> str:
        return super().getThumbnail()

    def getTags(self) -> str:
        tags: List[str] = list()
        for i in self._soup.find_all(name="category"):
            # lets vsc see the expected class
            i: BeautifulSoup = i
            tags.append(i.text)

        s = str(tags)
        return s

    def getLink(self) -> str:
        url: str = self._soup.find(name="link").next
        url = url.replace("\n", "")
        url = url.replace("\t", "")
        url = url.replace("\r", "")
        url = url.strip()
        return url


class JsonParser(RssFeedInterface):
    _url: str
    _siteName: str
    _sourceId: str
    _logger: LoggerInterface
    _soup: Dict

    def __init__(self,  _logger: LoggerInterface, url: str, siteName: str, sourceId: str):
        self._logger = _logger
        self._url: str = url
        self._siteName: str = siteName
        self.rc = RequestArticleContent(url=url)
        self.rc.getPageDetails()
        self.json = loads(self.rc.__source__)
        self._sourceId: str = sourceId

    def collectItems(self) -> List:
        return self._soup["items"]

    def processItem(self, item: Dict) -> Articles:
        exists = ArticlesTable().getByUrl(url=item["url"])
        if exists.id == '':

            a = Articles(
                tags=self.getTags(),
                title=self.getTitle(),
                url=self.getLink(),
                pubDate=self.getPublishDate(),
                thumbnail=self.getThumbnail(),
                authorName=self.getAuthorName(),
                description=self.getDescription(),
                sourceId=self.sourceId
            )
        return a

    def getTitle(self) -> str:
        return self._soup["title"]

    def getAuthorName(self) -> str:
        return self._soup["author"]["name"]

    def getPublishDate(self) -> str:
        return self._soup["date_published"]

    def getDescription(self) -> str:
        return self._soup["content_html"]

    def getThumbnail(self) -> str:
        rc = RequestContent(url=self.getLink())
        rc.getPageDetails()
        return rc.findArticleThumbnail()

    def getTags(self) -> str:
        return f"RSS, {self.siteName}"

    def getLink(self) -> str:
        return self._soup['url']
