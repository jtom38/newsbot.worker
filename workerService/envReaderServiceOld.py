from typing import List
from dotenv import load_dotenv
from pathlib import Path
from workerInfra.models import (
    EnvDiscordDetails
    ,EnvRssDetails
    ,EnvYoutubeConfig
    ,EnvYoutubeDetails
    ,EnvRedditConfig
    ,EnvRedditDetails
    ,EnvTwitterConfig
    ,EnvTwitterDetails
    ,EnvTwitchConfig
    ,EnvTwitchDetails
    ,EnvFinalFantasyXIVDetails
    ,EnvPhantasyStarOnline2Details
    ,EnvPokemonGoDetails
    ,EnvInstagramDetails
)
from workerInfra.domain import EnvReaderInterface
import os


class EnvDiscordReader(EnvReaderInterface):
    def read(self) -> List[EnvDiscordDetails]:
        links: List[EnvDiscordDetails] = list()
        i = 0
        while i <= 9:
            edd = EnvDiscordDetails(
                name=os.getenv(f"NEWSBOT_DISCORD_{i}_NAME"),
                server=os.getenv(f"NEWSBOT_DISCORD_{i}_SERVER"),
                channel=os.getenv(f"NEWSBOT_DISCORD_{i}_CHANNEL"),
                url=os.getenv(f"NEWSBOT_DISCORD_{i}_URL"),
            )
            i = i + 1
            if edd.url != None:
                links.append(edd)
        return links


class EnvRssReader(EnvReaderInterface):
    def __init__(self) -> None:
        pass

    def read(self) -> List[EnvRssDetails]:
        links: List[EnvRssDetails] = list()
        i = 0
        while i <= 9:
            erd = EnvRssDetails(
                name=os.getenv(f"NEWSBOT_RSS_{i}_NAME"),
                url=os.getenv(f"NEWSBOT_RSS_{i}_URL"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_RSS_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if erd.name != None:
                links.append(erd)
        return links


class EnvYoutubeConfigReader(EnvReaderInterface):
    def read(self) -> EnvYoutubeConfig:
        eyc = EnvYoutubeConfig(
            debugScreenshots = self.__parseBool__("NEWSBOT_YOUTUBE_DEBUG_SCREENSHOTS")
        )
        return eyc


class EnvYoutubeReader(EnvReaderInterface):
    def read(self) -> List[EnvYoutubeDetails]:
        links: List[EnvYoutubeDetails] = list()
        i = 0
        while i <= 9:
            eytd = EnvYoutubeDetails(
                name=os.getenv(f"NEWSBOT_YOUTUBE_{i}_NAME"),
                url=os.getenv(f"NEWSBOT_YOUTUBE_{i}_URL"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_YOUTUBE_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if eytd.name != None:
                links.append(eytd)
        return links


class EnvRedditConfigReader(EnvReaderInterface):
    def read(self) -> EnvRedditConfig:
        item = EnvRedditConfig(
            allowNsfw = self.__parseBool__("NEWSBOT_REDDIT_ALLOW_NSFW")
            ,pullHot = self.__parseBool__("NEWSBOT_REDDIT_PULL_HOT")
            ,pullTop = self.__parseBool__("NEWSBOT_REDDIT_PULL_TOP")
        )
        return item


class EnvRedditReader(EnvReaderInterface):
    def read(self) -> List[EnvRedditDetails]:
        links: List[EnvRedditDetails] = list()
        i = 0
        while i <= 9:
            item = EnvRedditDetails(
                subreddit=os.getenv(f"NEWSBOT_REDDIT_{i}_SUBREDDIT"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_REDDIT_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.subreddit != None:
                links.append(item)
        return links


class EnvTwitchConfigReader(EnvReaderInterface):
    def read(self) -> EnvTwitchConfig:
        item = EnvTwitchConfig(
            clientId=os.getenv("NEWSBOT_TWITCH_CLIENT_ID"),
            clientSecret=os.getenv("NEWSBOT_TWITCH_CLIENT_SECRET"),
            monitorClips=self.__parseBool__(envFlag="NEWSBOT_TWITCH_MONITOR_CLIPS"),
            monitorLiveStreams=self.__parseBool__(envFlag="NEWSBOT_TWITCH_MONITOR_LIVE_STREAMS"),
            monitorVod=self.__parseBool__(envFlag="NEWSBOT_TWITCH_MONITOR_VOD"),
        )
        return item


class EnvTwitchReader(EnvReaderInterface):
    def read(self) -> List[EnvTwitchDetails]:
        links: List[EnvTwitchDetails] = list()
        i = 0
        while i <= 9:
            item = EnvTwitchDetails(
                user=os.getenv(f"NEWSBOT_TWITCH_{i}_USER"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_TWITCH_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.user != None:
                links.append(item)
        return links


class EnvTwitterConfigReader(EnvReaderInterface):
    def read(self) -> EnvTwitterConfig:
        item = EnvTwitterConfig(
            apiKey=os.getenv(f"NEWSBOT_TWITTER_API_KEY"),
            apiKeySecret=os.getenv(f"NEWSBOT_TWITTER_API_KEY_SECRET"),
            preferredLang=os.getenv(f"NEWSBOT_TWITTER_PREFERRED_LANG"),
            ignoreRetweet=self.__parseBool__(envFlag=f"NEWSBOT_TWITTER_IGNORE_RETWEET")
        )
        return item


class EnvTwitterReader(EnvReaderInterface):
    def read(self) -> List[EnvTwitterDetails]:
        links: List[EnvTwitterDetails] = list()
        i = 0
        while i <= 9:
            item = EnvTwitterDetails(
                name=os.getenv(f"NEWSBOT_TWITTER_{i}_NAME"),
                type=os.getenv(f"NEWSBOT_TWITTER_{i}_TYPE"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_TWITTER_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.name != None:
                links.append(item)
        return links


class EnvInstagramReader(EnvReaderInterface):
    def read(self) -> List[EnvInstagramDetails]:
        links: List[EnvInstagramDetails] = list()
        i = 0
        while i <= 9:
            item = EnvInstagramDetails(
                name=os.getenv(f"NEWSBOT_INSTAGRAM_{i}_NAME"),
                type=os.getenv(f"NEWSBOT_INSTAGRAM_{i}_TYPE"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_INSTAGRAM_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.name != None:
                links.append(item)
        return links


class EnvPokemonGoReader(EnvReaderInterface):
    def read(self) -> EnvPokemonGoDetails:
        item = EnvPokemonGoDetails(
            enabled=self.__parseBool__(envFlag=f"NEWSBOT_POGO_ENABLED"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_POGO_LINK_DISCORD")
            ),
        )
        return item


class EnvPhantasyStarOnline2Reader(EnvReaderInterface):
    def read(self) -> EnvPhantasyStarOnline2Details:
        return EnvPhantasyStarOnline2Details(
            enabled=self.__parseBool__(envFlag=f"NEWSBOT_PSO2_ENABLED"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_PSO2_LINK_DISCORD")
            ),
        )


class EnvFinalFantasyXIVReader(EnvReaderInterface):
    def read(self) -> EnvFinalFantasyXIVDetails:
        return EnvFinalFantasyXIVDetails(
            #allEnabled=self.__parseBool__("NEWSBOT_FFXIV_ALL"),
            topicsEnabled=self.__parseBool__(envFlag=f"NEWSBOT_FFXIV_TOPICS"),
            noticesEnabled=self.__parseBool__(envFlag=f"NEWSBOT_FFXIV_NOTICES"),
            maintenanceEnabled=self.__parseBool__(envFlag=f"NEWSBOT_FFXIV_MAINTENANCE"),
            updateEnabled=self.__parseBool__(envFlag=f"NEWSBOT_FFXIV_UPDATES"),
            statusEnabled=self.__parseBool__(envFlag=f"NEWSBOT_FFXIV_STATUS"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_FFXIV_LINK_DISCORD")
            ),
        )

class EnvReaderService():
    def __init__(self, loadEnvFile = True) -> None:
        if loadEnvFile == True: 
            load_dotenv(dotenv_path=Path(".env"))

        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 30
        self.discordTableCheckSeconds: int = 60 * 5
        self.threadSleepTimer: int = 60 * 30

        self.pogo_values: EnvPokemonGoDetails = EnvPokemonGoReader().read()
        self.pso2_values: EnvPhantasyStarOnline2Details = EnvPhantasyStarOnline2Reader().read()
        self.ffxiv_values: EnvFinalFantasyXIVDetails = EnvFinalFantasyXIVReader().read()
        
        self.reddit_values: List[EnvRedditDetails] = EnvRedditReader().read()
        self.reddit_config: EnvRedditConfig = EnvRedditConfigReader().read()

        self.youtube_values: List[EnvYoutubeDetails] = EnvYoutubeReader().read()
        self.youtube_config: EnvYoutubeConfig = EnvYoutubeConfigReader().read()
        self.instagram_values: List[EnvInstagramDetails] = EnvInstagramReader().read()
        
        self.twitter_values: List[EnvTwitterDetails] = EnvTwitterReader().read()
        self.twitter_config: EnvTwitterConfig = EnvTwitterConfigReader().read()

        self.twitch_values: List[EnvTwitchDetails] = EnvTwitchReader().read()
        self.twitch_config: EnvTwitchConfig = EnvTwitchConfigReader().read()

        self.rss_values: List[EnvRssDetails] = EnvRssReader().read()

        self.discord_values: List[EnvDiscordDetails] = EnvDiscordReader().read()