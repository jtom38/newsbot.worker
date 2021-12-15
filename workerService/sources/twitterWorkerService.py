from workerInfra.models import Articles, Sources, EnvTwitterConfig
from workerInfra.enum import SourcesEnum
from workerInfra.domain import SourcesInterface, SourceParseInterface, DriverInterface, LoggerInterface
from workerInfra.base import ParserBase, SourcesBase
from workerService.db import ArticlesTable
from workerService import CacheFactory, SqlCache, FirefoxDriverService
from workerService.logger import BasicLoggerService
from tweepy import AppAuthHandler, API, Cursor
from typing import List
import tweepy
from os import getenv


class TweetParser(SourceParseInterface, ParserBase):
    _logger: LoggerInterface
    _driver: DriverInterface

    def __init__(self) -> None:
        self._logger = BasicLoggerService()
        self._driver: DriverInterface = FirefoxDriverService(self._logger)
        pass

    def start(self, tweet: object, sourceId: str, searchValue: str):
        if sourceId == '':
            raise Exception("SourceID is missing")

        if tweet.id_str == "":
            raise Exception("The reqested tweet to parse had a invalid ID.")

        self.exists: bool = False
        self.__tweet__ = tweet
        self.article = self.__newArticle__()

        self.article.url = self.getUrl()
        if self.articleExists() is True:
            self.article = self.__newArticle__()
            self.exists = True
            return None

        try:
            self.article.sourceId = sourceId
            self.article.authorName = self.getAuthorName(tweet)
            self.article.authorImage = self.getAuthorImage(tweet)
            self.article.description = self.getDescription(tweet)
            self.article.tags = self.getTags(searchValue)
            self.article.pubDate = self.getPublishDate()
            self.article.thumbnail = self.getThumbnail()
            if self.article.thumbnail == '':
                self.article.thumbnail = self.getImages(self.article.url)
        except Exception as e:
            self._logger.error(f"Failed to parse '{self.article.url}'.  Skipping over the object. Error: {e}")

    def __newArticle__(self) -> Articles:
        return Articles()

    def getAuthorImage(self, tweet: object) -> str:
        try:
            return tweet.author.profile_image_url
        except Exception as e:
            msg = f"Failed to find the tweet author screen name. Error: {e}"
            self._logger.error(msg)
            raise Exception(msg)

    def getAuthorName(self, tweet: object) -> str:
        try:
            screenName: str = tweet.author.screen_name
            name: str = tweet.author.name
            return f"{name} @{screenName}"
        except Exception as e:
            self._logger.error(f"Failed to find the tweet author. Error: {e}")
            raise Exception(f"Failed to find the tweet author. Error: {e}")

    def getDescription(self, tweet: object) -> str:
        try:
            d = tweet.text
            return d
        except Exception as e:
            self._logger.error(f"Attempted to pull tweet description, but failed. Error: {e}")

    def getUrl(self) -> str:
        # a.url = f"https://twitter.com/{authorScreenName}/status/{tweet.id}"
        try:
            name = self.__tweet__.author.screen_name
            return f"https://twitter.com/{name}/status/{self.__tweet__.id}"
        except Exception as e:
            self._logger.error(f"Failed to generate tweet url. {e}")

    def getThumbnail(self) -> str:
        try:
            if len(self.__tweet__.entities['media']) == 0:
                return ""

            for img in self.__tweet__.entities["media"]:
                if "photo" in img["type"] and "twimg" in img["media_url"]:
                    return img["media_url"]
        except Exception as e:
            self._logger.warning(f"Unable to find thumbnail. {e}")
            # I expect that this wont be found a lot, its not a problem.
            return ""

    def getPublishDate(self) -> str:
        try:
            return str(self.__tweet__.created_at)
        except Exception as e:
            self._logger.error(
                f"Failed to find 'created_at' on the tweet. \r\nError: {e}"
            )

    def getTags(self, searchValue: str) -> str:
        try:
            tags = f"twitter, {searchValue}, "
            for t in self.__tweet__.entities["hashtags"]:
                tags += f"{t['text']}, "
            return tags
        except Exception as e:
            self._logger.error(
                f"Failed to find 'hashtags' on the tweet. \r\nError: {e}"
            )

    def getImages(self, url: str) -> str:
        try:
            # The API does not seem to expose all images attached to the tweet.. why idk.
            # We are going to try with Chrome to find the image.
            # It will try a couple times to try and find the image given the results are so hit and miss.
            album: str = ""
            self._driver.goTo(url)
            source = self._driver.getContent()
            soup = self.getParser(seleniumContent=source)
            images = soup.find_all(name="img")  # attrs={"alt": "Image"})
            for img in images:
                try:
                    # is the image in a card
                    if "card_img" in img.attrs["src"]:
                        return img.attrs["src"]

                    if img.attrs["alt"] == "Image":
                        album += f"{img.attrs['src']} "
                        # a.thumbnail = img.attrs['src']
                        # break
                except Exception as e:
                    self._logger.warning(f"Unable to find images in the tweet. Error: {e}")
                    pass

            return album
        except Exception as e:
            self._logger.warning("Failed to collect images.", e)
            pass
        pass

    def articleExists(self) -> bool:
        res = ArticlesTable().getByUrl(self.article.url)
        if res.id == '':
            return False

        return True


class TwitterWorkerService(SourcesBase, SourcesInterface):
    _logger: LoggerInterface
    _parser: TweetParser

    def __init__(self):
        self._logger = BasicLoggerService()
        self._parser = TweetParser()
        self.cache = CacheFactory(SqlCache())
        self.settings = EnvTwitterConfig(
            apiKey=getenv('NEWSBOT_TWITTER_API_KEY'),
            apiKeySecret=getenv("NEWSBOT_TWITTER_API_KEY_SECRET"),
            ignoreRetweet=self.cache.findBool("twitter.ignore.retweet"),
            preferredLang=self.cache.find("twitter.preferred.lang")
        )
        self.setSiteName(SourcesEnum.TWITTER)
        self.uri: str = "https://twitter.com"
        self.baseUri = self.uri

    def getArticles(self) -> List[Articles]:
        if self.settings.apiKey == "":
            raise Exception("NEWSBOT_TWITTER_API_KEY is missing a value")

        if self.settings.apiKeySecret == "" or self.settings.apiKeySecret is None:
            raise Exception("NEWSBOT_TWITTER_API_KEY_SECRET is missing a value")

        self._parser._driver.start()
        allArticles: List[Articles] = list()

        api = self.login()

        for _site in self.__links__:
            site: Sources = _site
            self.setActiveSource(source=SourcesEnum.TWITTER, name=site.name, sourceType=site.type)
            self._logger.info(
                f"Twitter - {site.type} - {site.name} - Checking for updates."
            )

            # Figure out if we are looking for a user or tag
            if site.type == "user":
                tweets = self.getTweets(api=api, username=site.name)
                if len(tweets) == 0:
                    continue
                articles = self.convertTweetsToArticles(tweets=tweets, searchValue=site.name, isHashtag=False)

            elif site.type == "tag":
                tweets = self.getTweets(api=api, hashtag=site.name)
                if len(tweets) == 0:
                    continue
                articles = self.convertTweetsToArticles(tweets=tweets, searchValue=site.name, isHashtag=True)

            for i in articles:
                allArticles.append(i)

        self._parser._driver.close()
        return allArticles

    def getTweets(self, api: API, username: str = "", hashtag: str = "") -> List:
        tweets = list()

        try:
            if username != "":
                for tweet in Cursor(api.user_timeline, id=username).items(15):
                    tweets.append(tweet)

            if hashtag != "":
                for tweet in Cursor(api.search, q=f"#{hashtag}").items(15):
                    tweets.append(tweet)
        except Exception as e:
            self._logger.error(f"{e}")
        finally:
            return tweets

    def login(self) -> API:
        appAuth = AppAuthHandler(consumer_key=self.settings.apiKey, consumer_secret=self.settings.apiKeySecret)
        try:
            api = API(appAuth)
            return api
        except Exception as e:
            self._logger.critical(f"Failed to authenicate with Twitter. Error: {e}")
            return list()

    def convertTweetsToArticles(self, tweets: List, searchValue: str, isHashtag: bool) -> List[Articles]:
        _list = list()
        for tweet in tweets:
            lang = self.settings.preferredLang
            if lang == "None":
                pass
            elif tweet.lang == lang:
                pass
            elif tweet.lang != lang:
                continue

            # Checking if this is a retweet
            isRetweet = self.__isRetweet__(tweet)
            if isRetweet is True:
                continue

            self._parser.start(tweet=tweet, sourceId=self.getActiveSourceID(), searchValue=searchValue)
            if self._parser.exists is True:
                continue

            _list.append(self._parser.article)

        return _list

    def getTweetUrl(self, tweet: object) -> str:
        url: str = ""
        try:
            url = tweet.entities["urls"][0]["expanded_url"]
        except Exception as e:
            self._logger.debug(f"Failed to find the URL to the exact tweet. Checking the second location. Error: {e}")
            pass

        # if the primary locacation fails, try this location
        if url == "":
            try:
                url = tweet.entities["media"][0]["expanded_url"]
            except Exception as e:
                self._logger.debug(f"Failed to find the tweet url in 'entities['media'][0]['expanded_url']. Error: {e}")
                pass

        # if its a retweet look here
        if url == "":
            try:
                url = tweet.retweeted_status.entities["urls"][0]["expanded_url"]
            except Exception as e:
                self._logger.debug(f"retweet did not contain entities.urls. Error: {e}")
                pass

        if url == "":
            try:
                url = tweet.retweeted_status.entities["media"][0]["expanded_url"]
            except Exception as e:
                self._logger.debug(f"retweet did not contain entities.media. Error: {e}")
                pass
        return url

    def __isRetweet__(self, tweet) -> bool:
        """
        Returns
        True if we need to skip
        False if we move forward
        """
        ignoreRetweet = self.settings.ignoreRetweet

        if self.settings.ignoreRetweet is True and tweet.in_reply_to_screen_name is not None:
            return True

        if ignoreRetweet is True:
            text: str = tweet.text
            if text.startswith("RT ") is True:
                return True
            else:
                return False
        else:
            return False
