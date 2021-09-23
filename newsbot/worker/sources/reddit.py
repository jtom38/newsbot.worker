from newsbot.core.cache import Cache
from typing import List
from json import loads
from bs4 import BeautifulSoup
from newsbot.core.logger import Logger
from newsbot.core.constant import SourceName
from newsbot.core.sql import Articles, Sources, DiscordWebHooks
from newsbot.worker.sources.common import *
from time import sleep, time


class RedditPostPreviewImage():
    """
    This contains the images attached with the post
    """
    id: str
    imageUrl: str
    imageWidth: int
    imageHeight: int


class RedditPostPreview():
    """
    This contains the preview items of a reddit object.
    """
    images: List[RedditPostPreviewImage]


class RedditPostMediaRedditVideo():
    """
    This contains the information about the video hosted on the reddit platform
    """
    bitrateKbps: int
    fallbackUrl: str
    height: int
    width: int
    duration: int
    transcodingStatus: str


class RedditPostMedia():
    """
    This contains the video details attached to the post
    """
    reddit_video = RedditPostMediaRedditVideo()


class RedditPost():
    """
    This contains a subset of all the properties that can be found in the Reddit Json.  
    """
    subreddit: str
    #subreddit_id: str
    selftext: str
    author: str
    #saved: bool
    title: str
    nsfw: bool 
    #locked: bool
    #numberOfComments: int
    permalink: str
    thumbnail: str
    preview: List[RedditPostPreview]
    media: RedditPostMedia
    pass

    def __init__(self, data: dict) -> None:
        self.subreddit = data['subreddit']
        self.selftext = data['selftext']
        self.author = data['author']
        self.permalink = data['permalink']
        self.nsfw = data['over_18']
        self.thumbnail = data['thumbnail']
        if len(data['preview']) == 0:
            self.preview = list()
        else:
            self.preview = self.__convertPreview__(data['preview'])

        if len(data['media']) == 0:
            self.media = RedditPostMedia()
        else:
            self.media = self.__convertPreview__(data['media'])

    def __convertPreview__(self, preview: dict) -> List[RedditPostPreview]:
        l = list()
        if len(preview) == 0:
            return l

        try:
            for i in preview:
                p = RedditPostPreview()
                p.id = i['id']
                p.imageHeight = i['source']['height']
                p.imageWidth = i['source']['width']
                p.imageUrl = i['source']['url']
                l.append(p)

            return l
        except:
            pass
        
    def __convertPreviewImages__(self):
        pass

    def __convertMedia__(self, media: dict) -> None:
        r = RedditPostMedia()
        if len(media) > 0:

            return r
        try:
            m = media['reddit_video']
            r.reddit_video.bitrateKbps = m['bitrate_kbps']
            r.reddit_video.duration = m['duration']
            r.reddit_video.fallbackUrl = m['fallback_url']
            r.reddit_video.height = m['height']
            r.reddit_video.width = m['width']
            r.reddit_video.transcodingStatus = m['transcoding_status']
            return r
        except:
            pass


class RedditReader(BaseSources, BFirefox, ISources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.cache = Cache()
        self.uri = "https://reddit.com/r/aww/top.json"
        self.setSiteName(SourceName.REDDIT)
        self.settingNsfwAllowed: bool = bool(self.cache.findBool(key="reddit.allow.nsfw"))
        self.settingPullTop: bool = bool(self.cache.findBool("reddit.pull.top"))
        self.settingPullHot: bool = bool(self.cache.findBool("reddit.pull.hot"))

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for source in self.__links__:
            self.setActiveSource(SourceName.REDDIT, name = source.name)
            subreddit = source.name
            self.logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            # Add the info we get via Selenium to the Cache to avoid pulling it each time.
            authorName = self.cache.find(key=f"reddit.{subreddit}.authorName")
            if authorName == "":
                self.cachePageDetails(subreddit)
                authorName = self.cache.find(key=f"reddit.{subreddit}.authorName")

            authorImage = self.cache.find(key=f"reddit.{subreddit}.authorImage")

            # Now check the RSS/json
            posts = self.getPosts(subreddit)
            for p in posts:
                #exists = self.articlesTable.getByUrl(url=f"https://reddit.com{p['data']['permalink']}")
                #if exists.id == '':
                
                # Checking if NFSW posts can be sent
                if p['data']['over_18'] == True and self.settingNsfwAllowed == False:
                    continue

                post = self.getPostDetails(p["data"], authorName, authorImage )
                allArticles.append(post)

            sleep(5.0)

        return allArticles

    def cachePageDetails(self, subreddit: str) -> None:
        self.driver = self.driverStart()
        soup = self.getSubRedditSoup(subreddit)
        subTagline = self.findTagline(soup)
        if subTagline != "":
            authorName = f"/r/{subreddit} - {subTagline}"
        else:
            authorName = f"/r/{subreddit}"
        self.cache.add(key=f"reddit.{subreddit}.authorName", value=authorName)

        authorImage = self.findSubThumbnail(soup)
        self.cache.add(key=f"reddit.{subreddit}.authorImage", value=authorImage)
        self.driverClose()
        pass

    def getSubRedditSoup(self, subreddit: str) -> BeautifulSoup:
        # Collect values that we do not get from the RSS
        uri = f"https://www.reddit.com/r/{subreddit}/"
        self.driverGoTo(uri)
        soup = self.getParser(seleniumContent=self.driverGetContent())
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
            self.logger.critical(f"Failed to find the subreddit name in the html. Error {e}")
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

        if self.settingPullHot == False and self.settingPullTop == False:
            self.settingPullTop = True

        jsonUrl: str = ''
        if self.settingPullHot == True:
            jsonUrl = f"{rootUri}.json"

        if self.settingPullTop == True:
            jsonUrl = f"{rootUri}/top.json"

        self.logger.debug(f"Collecting posts from {jsonUrl}")
        try:
            siteContent = self.getContent(jsonUrl)
            page = self.getParser(requestsContent=siteContent)
            json = loads(page.text)
            items = json["data"]["children"]
            if len(items) <= 24:
                self.logger.critical(f"Was able to reach out to '{jsonUrl}' but it returned less or no posts!")
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
                self.logger.warning(f"Found 'media_only' object. url: {a.url}")
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
                    self.logger.error(
                        f"Failed to find the images on a reddit gallery.  CSS might have changed."
                    )
            else:
                a.thumbnail = obj["url"]

            return a
        except Exception as e:
            self.logger.error(
                f"Failed to extract Reddit post.  Too many connections? {e}"
            )
