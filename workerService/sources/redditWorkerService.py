from workerInfra.domain.driverInterface import DriverInterface
from workerInfra.domain.loggerInterface import LoggerInterface
from workerInfra.enum import SourcesEnum
from workerInfra.models import Articles, EnvRedditConfig
from workerInfra.domain import SourcesInterface
from workerInfra.base import SourcesBase
from workerService import FirefoxDriverService
from workerService.logger import BasicLoggerService
from workerService.cache import Cache, CacheFactory
from typing import List
from time import sleep
from bs4 import BeautifulSoup
from json import loads


class RedditWorkerService(SourcesBase, FirefoxDriverService, SourcesInterface):
    _logger: LoggerInterface
    _driver: DriverInterface
    _cache: CacheFactory

    def __init__(self) -> None:
        self._logger = BasicLoggerService()
        self._cache = Cache()
        self._driver = FirefoxDriverService(self._logger)
        self.uri = "https://reddit.com/r/aww/top.json"
        self.setSiteName(SourcesEnum.REDDIT)
        self.config = EnvRedditConfig(
            allowNsfw= bool(self._cache.findBool(key="reddit.allow.nsfw")),
            pullTop= bool(self._cache.findBool("reddit.pull.top")),
            pullHot= bool(self._cache.findBool("reddit.pull.hot"))
        )

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for source in self.__links__:
            self.setActiveSource(SourcesEnum.REDDIT, name = source.name)
            subreddit = source.name
            self._logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            # Add the info we get via Selenium to the Cache to avoid pulling it each time.
            authorName = self._cache.find(key=f"reddit.{subreddit}.authorName")
            if authorName == "":
                self._cachePageDetails(subreddit)
                authorName = self._cache.find(key=f"reddit.{subreddit}.authorName")

            authorImage = self._cache.find(key=f"reddit.{subreddit}.authorImage")

            # Now check the RSS/json
            posts = self.getPosts(subreddit)
            for p in posts:
                #exists = self.articlesTable.getByUrl(url=f"https://reddit.com{p['data']['permalink']}")
                #if exists.id == '':
                
                # Checking if NFSW posts can be sent
                if p['data']['over_18'] == True and self.config.allowNsfw == False:
                    continue

                post = self.getPostDetails(p["data"], authorName, authorImage )
                allArticles.append(post)

            sleep(5.0)

        return allArticles

    def cachePageDetails(self, subreddit: str) -> None:
        self._driver = self._driverStart()
        self.__driver__ = self._driver
        soup = self.getSubRedditSoup(subreddit)
        subTagline = self.findTagline(soup)
        if subTagline != "":
            authorName = f"/r/{subreddit} - {subTagline}"
        else:
            authorName = f"/r/{subreddit}"
        self._cache.add(key=f"reddit.{subreddit}.authorName", value=authorName)

        authorImage = self.findSubThumbnail(soup)
        self._cache.add(key=f"reddit.{subreddit}.authorImage", value=authorImage)
        self._driverClose()
        pass

    def getSubRedditSoup(self, subreddit: str) -> BeautifulSoup:
        # Collect values that we do not get from the RSS
        uri = f"https://www.reddit.com/r/{subreddit}/"
        self._driverGoTo(uri)
        soup = self.getParser(seleniumContent=self._driverGetContent())
        return soup

    def findSubThumbnail(self, soup: BeautifulSoup) -> str:
        authorImage: str = ""

        #Find the 
        subImages = soup.find_all(name="img", attrs={"class": "Mh_Wl6YioFfBc9O1SQ4Jp"})

        if len(subImages) != 0:
            # Failed to find the custom icon.  The sub might not have a custom CSS.
            authorImage = subImages[0].attrs["src"]

        if authorImage == "":
            # I am not sure how to deal with svg images at this time.  
            # Going to throw in the default reddit icon.
            subImages = soup.find_all(
                name="svg", attrs={"class": "ixfotyd9YXZz0LNAtJ25N"}
            )
            if len(subImages) == 1:
                authorImage = "https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png"
        return authorImage

    def findTagline(self, soup: BeautifulSoup) -> str:
        tagLine: str = ''
        try:
            subName = soup.find_all(name="h1", attrs={"class": "_2yYPPW47QxD4lFQTKpfpLQ"} )
            tagLine = subName[0].text
            assert subName[0].text
        except Exception as e:
            self._logger.critical(f"Failed to find the subreddit name in the html. Error {e}")
        return tagLine

    def getVideoThumbnail(self, preview) -> str:
        try:
            return preview["images"][0]["source"]["url"]
        except:
            return ""

    def getPosts(self, subreddit: str) -> List[dict]:
        """
        This uses requests to go and collect the json from the reddit url given.
        """
        if subreddit == '':
            raise Exception("Unable to collect posts from an unknown subreddit.  Please define the subreddit to collect form.")
        rootUri = f"https://reddit.com/r/{subreddit}"

        if self.config.pullHot == False and self.config.pullTop == False:
            self.settingPullTop = True

        jsonUrl: str = ''
        if self.config.pullHot == True:
            jsonUrl = f"{rootUri}.json"

        if self.config.pullTop == True:
            jsonUrl = f"{rootUri}/top.json"

        self._logger.debug(f"Collecting posts from {jsonUrl}")
        try:
            siteContent = self.getContent(jsonUrl)
            page = self.getParser(requestsContent=siteContent)
            json = loads(page.text)
            items = json["data"]["children"]
            if len(items) <= 24:
                self._logger.critical(f"Was able to reach out to '{jsonUrl}' but it returned less or no posts!")
            else:
                return items
        except:
            raise Exception(f"Failed to connect to {jsonUrl}.")

    def getPostDetails(self, obj: dict, authorName: str, authorImage: str) -> Articles:
        try:
            a = Articles(
                url=f"https://reddit.com{obj['permalink']}",
                authorName=authorName,
                authorImage=authorImage,
                title=obj['title'],
                tags=obj["subreddit"],
                sourceId=self.__activeRecord__.id
            )

            # figure out what url we are going to display
            if obj["is_video"] == True:
                a.video = obj["media"]["reddit_video"]["fallback_url"]
                a.videoHeight = obj["media"]["reddit_video"]["height"]
                a.videoWidth = obj["media"]["reddit_video"]["width"]
                a.thumbnail = self.getVideoThumbnail(obj["preview"])

            elif obj["media_only"] == True:
                self._logger.warning(f"Found 'media_only' object. url: {a.url}")
            elif "gallery" in obj["url"]:
                self.uri = obj["url"]
                source = self.getContent()
                soup = self.getParser(requestsContent=source)
                try:
                    images = soup.find_all(
                        name="img", attrs={"class": "_1dwExqTGJH2jnA-MYGkEL-"}
                    )
                    pictures: str = ""
                    for i in images:
                        pictures += f"{i.attrs['src']} "
                    a.thumbnail = pictures
                except Exception as e:
                    self._logger.error(
                        f"Failed to find the images on a reddit gallery.  CSS might have changed."
                    )
            else:
                a.thumbnail = obj["url"]

            return a
        except Exception as e:
            self._logger.error(
                f"Failed to extract Reddit post.  Too many connections? {e}"
            )
