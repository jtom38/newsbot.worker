from typing import List
from newsbotWorker.infra import models
from newsbotWorker.service.logger import Logger
from newsbotWorker.service.cache import Cache
from newsbotWorker.infra.enum import SourcesEnum
from newsbotWorker.service import TwitchAPI
from newsbotWorker.infra.models import TwitchVideo, TwitchUser, TwitchClip
from newsbotWorker.infra.base import SourcesBase
from newsbotWorker.infra.domain import SourcesInterface
from newsbotWorker.infra.models import Articles, EnvTwitchConfig


class TwitchWorkerService(SourcesBase, SourcesInterface):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.cache = Cache()
        self.settings = EnvTwitchConfig(
            clientId=''
            ,clientSecret=''
            ,monitorClips= self.cache.findBool(key="twitch.clips.enabled")
            ,monitorLiveStreams=False
            ,monitorVod= self.cache.findBool(key="twitch.vod.enable")

        )
        self.setSiteName(SourcesEnum.TWITCH)
        self.uri = "https://twitch.tv/"
        pass

    def getArticles(self) -> List[Articles]:
        self.logger.debug("Checking Twitch for updates.")
        self.api = TwitchAPI()
        self.auth = self.api.auth()

        allPosts = list()
        for i in self.__links__:
            self.setActiveSource(source=SourcesEnum.TWITCH, name=i.name)
            userName = i.name
            self.logger.debug(f"Checking Twitch user {userName} for updates.")

            self.cacheUserId(userName=userName)

            # We have cached this information already
            user_id = self.cache.find(key=f"twitch.{userName}.user_id")
            display_name = self.cache.find(key=f"twitch.{userName}.display_name")
            profile_image_url = self.cache.find(key=f"twitch.{userName}.profile_image_url")

            if self.settings.monitorClips is True:
                clips: List[TwitchClip] = self.api.getClips(self.auth, user_id=user_id)
                for v in clips:
                    try:
                        a = Articles(
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"twitch, clip, {display_name}",
                            title=v.title,
                            pubDate=v.created_at,
                            url=v.url,
                            thumbnail=v.thumbnail_url,
                            description="A new clip has been posted! You can watch it with the link below.",
                            sourceId=self.getActiveSourceID()
                        )
                        allPosts.append(a)
                    except Exception as e:
                        self.logger.error(e)

            if self.settings.monitorVod is True:
                videos: List[TwitchVideo] = self.api.getVideos(self.auth, user_id=user_id)
                for v in videos:
                    try:
                        a = Articles(
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"twitch, vod, {display_name}",
                            # description = v.description,
                            title=v.title,
                            description="A new video has been posed! You can watch it with the link below.",
                            pubDate=v.published_at,
                            url=v.url,
                            sourceId=self.getActiveSourceID()
                        )
                        thumb: str = v.thumbnail_url
                        thumb = thumb.replace("%{width}", "600")
                        thumb = thumb.replace("%{height}", "400")
                        a.thumbnail = thumb
                        allPosts.append(a)
                    except Exception as e:
                        self.logger.error(e)

        return allPosts

    def cacheUserId(self, userName: str) -> None:
        user_id = self.cache.find(key=f"twitch.{userName}.user_id")
        if user_id == "":
            # Take the value and add it to the cache so we dont need to call the API for this
            user: TwitchUser = self.api.getUser(self.auth, userName)
            user_id = self.cache.add(key=f"twitch.{userName}.user_id", value=user.id)
            self.cache.add(key=f"twitch.{userName}.display_name", value=user.display_name)
            self.cache.add(key=f"twitch.{userName}.profile_image_url", value=user.profile_image_url)
        else:
            pass
