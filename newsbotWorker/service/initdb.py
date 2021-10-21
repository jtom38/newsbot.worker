from newsbotWorker.infrastructure.models.envReader import *
from newsbotWorker.service.envreader import Env
from newsbotWorker.infrastructure.enum import SourcesEnum, SourceTypeEnum
#from newsbot.core.constant import SourcesSource, SourceType, SourcesSource
from typing import List
from abc import ABC, abstractclassmethod
from newsbotWorker.service.db import *
from newsbotWorker.infrastructure.models.db import *


class FailedToIUpdateSource(Exception):
    """
    This is raised when the source is checked and the results are null.
    """


class IUpdateSource(ABC):
    @abstractclassmethod
    def update(self, values) -> None:
        pass


class UpdateSource(IUpdateSource):
    def __init__(self) -> None:
        self.enableTables()

    def enableTables(self) -> None:
        self.sourceTable = SourcesTable()
        self.webHooksTable = DiscordWebHooksTable()
        self.sourceLinksTable = SourceLinksTable()

    def updateSourceLinks(self, source: Sources, hookNames: List[str]) -> None:
        try:
            for h in hookNames:
                l: DiscordWebHooks = self.webHooksTable.getByName(name=h)
                slTable = self.sourceLinksTable

                sl = SourceLinks(
                    discordName=f"{l.name}", 
                    discordID=l.id, 
                    SourcesSource=source.name, 
                    sourceType=source.source,
                    sourceID=source.id
                )
                slTable.update(sl)
                
        except Exception as e:
            print(f"Failed to update SourceLinks for {source.source} {source.name}. Error: {e}")

    def disableMissing(self, source: SourcesEnum) -> None:
        s = SourcesTable().getAllBySource(source.value)
        pass


class IUpdateSourceURL(ABC):
    @abstractclassmethod
    def __getUrl__(self, type:str, name: str) -> str:
        pass


class UpdateRSSSource(UpdateSource):
    SourcesSource: str = "rss"
    def update(self, values: List[EnvRssDetails]) -> None:
        for i in values:
            # collect the active record from the API
            a = self.sourceTable.getByNameAndSource(name=i.name, source='rss')

            # Generate the current object in memory
            current = Sources(
                site=i.name, name=i.name, source=SourcesEnum.RSS.value,
                url=i.url, fromEnv=True, enabled=True
            )
            # if we got the id from the API, use it 
            if a.id != '':
                current.id = a.id

            # Update the API with the new record
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=i.discordLinkName)

        s = SourcesTable().getAllBySource("rss")
        for i in s:
            if i.enabled == False:
                continue

            exists: bool = False
            for v in values:
                if i.name == v.name:
                    exists = True
                    
            if exists == False:
                i.enabled = False
                self.sourceTable.update(i)


class UpdateYoutubeSource(UpdateSource):
    SourcesSource: str = SourcesEnum.YOUTUBE.value
    def update(self, values: List[EnvYoutubeDetails]) -> None:
        for i in values:
            current =Sources(site=self.SourcesSource, name=i.name, source=self.SourcesSource, url=i.url, fromEnv=True)
            res = self.sourceTable.update(current)           
            self.updateSourceLinks(source=res, hookNames=i.discordLinkName)


class UpdateRedditSource(UpdateSource):
    SourcesSource: str = SourcesEnum.REDDIT.value
    def update(self, values: List[EnvRedditDetails]) -> None:
        for i in values:
            current = Sources(site=self.SourcesSource, name=i.subreddit, source=self.SourcesSource, url=f"https://reddit.com/r/{i.subreddit}/", fromEnv=True)
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=i.discordLinkName)


class UpdateTwitchSource(UpdateSource):
    SourcesSource: str = SourcesEnum.TWITCH.value
    def update(self, values: List[EnvTwitchDetails]) -> None:
        for i in values:
            current = Sources(site=self.SourcesSource, name=i.user, source=self.SourcesSource, url=f"https://twitch.tv/{i.user}/", fromEnv=True)
            res =self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=i.discordLinkName)


class UpdateTwitterSource(UpdateSource, IUpdateSourceURL): 
    SourcesSource: str = SourcesEnum.TWITTER.value
    def update(self, values: List[EnvTwitterDetails]) -> None:
        for i in values:
            current = Sources(site=self.SourcesSource, name=i.name, source=self.SourcesSource, type=i.type.lower(), 
                    url=self.__getUrl__(type=i.type.lower(), name=i.name),fromEnv=True
                )
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=i.discordLinkName)

    def __getUrl__(self, type: str, name: str) -> str:
        root: str = "https://twitter.com"
        if   type == "user": return f"{root}/{name}/"
        elif type == "tag":  return f"{root}/hashtag/{name}"
        else:                return root


class UpdateInstagramSource(UpdateSource, IUpdateSourceURL):
    SourcesSource: str = SourcesEnum.INSTAGRAM.value
    def update(self, values: List[EnvInstagramDetails]) -> None:
        for i in values:
            uri: str = self.__getUrl__(type=i.type.lower(), name=i.name)
            Sources(
                site=self.SourcesSource, name=i.name, source=self.SourcesSource, 
                type=i.type.lower(), url=uri, fromEnv=True
            )
            #self.sourceTable.update()
            #s = self.sourceTable.getBySourcesSourceType(name=i.name, source=SourcesEnum.INSTAGRAM.value, type=i.type)
            #self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

    def __getUrl__(self, type: str, name: str) -> str:
        root: str = "https://instagram.com"
        if type == "user":  return f"{root}/{name}/"
        elif type == "tag": return f"{root}/explore/tags/{name}"
        else:               return root


class UpdatePokemonGoHubSource(UpdateSource):
    SourcesSource: str = SourcesEnum.POKEMONGO.value
    def update(self, values: EnvPokemonGoDetails) -> None:
        try:
            current = Sources(
                site=self.SourcesSource,
                name=self.SourcesSource,
                source=self.SourcesSource,
                enabled=values.enabled,
                value='',
                tags='pokemongo',
                url="https://pokemongohub.net",
                fromEnv=True
            )
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enable 'Pokemon Go Hub' source. Error: {e}")


class UpdatePhantasyStarOnline2Source(UpdateSource):
    SourcesSource: str = SourcesEnum.PHANTASYSTARONLINE2.value
    def update(self, values: EnvPhantasyStarOnline2Details) -> None:
        try:
            current = Sources(
                site=self.SourcesSource,
                value='',
                tags='pso2',
                name=self.SourcesSource,
                source=self.SourcesSource,
                enabled=values.enabled,
                url="https://pso2.com",
                fromEnv=True
            )
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enabled 'Phantasy Star Online 2' source. Error: {e}")


class UpdateFinalFantasyXIVSource(UpdateSource):
    def __init__(self, topic: str, enabled: bool) -> None:
        self.topic: str = topic
        self.enabled: bool = enabled
        self.SourcesSource: str = SourcesEnum.FINALFANTASYXIV.value
        self.url: str = "https://finalfantasyxiv.com"
        self.enableTables()

    def update(self, values: EnvFinalFantasyXIVDetails) -> None:  
        try:
            current = Sources(
                site=self.SourcesSource,
                value='',
                tags='ffxiv',
                name=self.topic, 
                source=self.SourcesSource, 
                enabled=self.enabled, 
                url=self.url, 
                fromEnv=True
            )
            res = self.sourceTable.update(current)
            self.updateSourceLinks(source=res, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enabled '{self.topic}' in '{SourcesEnum.FINALFANTASYXIV.value}' source. Error: {e}")


class InitDb:
    def __init__(self) -> None:
        self.e = Env()
        self.enableTables()

    def enableTables(self) -> None:
        self.iconsTable = IconsTable()
        self.sourcesTable = SourcesTable()
        self.settingsTable = SettingsTable()
        self.discordWebHooksTable = DiscordWebHooksTable()

    def clearOldRecords(self) -> None:
        # clear our the table cache from last startup
        Sources().clearTable()
        DiscordWebHooks().clearTable()

    def addStaticIcons(self) -> None:
        table = self.iconsTable
        table.update(Icons(
            site=f"Default {SourcesEnum.POKEMONGO.value}", 
            filename="https://pokemongohub.net/wp-content/uploads/2017/04/144.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.PHANTASYSTARONLINE2.value}",
            filename="https://raw.githubusercontent.com/jtom38/newsbot/master/mounts/icons/pso2.jpg"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.FINALFANTASYXIV.value}", 
            filename="https://img.finalfantasyxiv.com/lds/h/0/U2uGfVX4GdZgU1jASO0m9h_xLg.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.REDDIT.value}",
            filename="https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.YOUTUBE.value}",
            filename="https://www.youtube.com/s/desktop/c46c1860/img/favicon_144.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.TWITTER.value}",
            filename="https://abs.twimg.com/responsive-web/client-web/icon-ios.8ea219d5.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.INSTAGRAM.value}",
            filename="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png"
        ))
        table.update(Icons(
            site=f"Default {SourcesEnum.TWITCH.value}",
            filename="https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png"
        ))

        # RSS based sites
        table.update(Icons(
            site="Default Engadget",
            filename="https://s.yimg.com/kw/assets/apple-touch-icon-120x120.png"
        ))
        table.update(Icons(
            site="Default GitHub",
            filename="https://github.githubassets.com/images/modules/open_graph/github-logo.png",
        ))

    def rebuildCache(
        self, twitchConfig: EnvTwitchConfig, 
        twitterConfig: EnvTwitterConfig, 
        redditConfig: EnvRedditConfig,
        youtubeConfig: EnvYoutubeConfig
        ) -> None:
        table = self.settingsTable
        table.update(Settings(key="twitch.clips.enabled", value=twitchConfig.monitorClips))
        table.update(Settings(key="twitch.vod.enabled", value=twitchConfig.monitorVod))
        table.update(Settings(key="twitch.livestreams.enabled", value=twitchConfig.monitorLiveStreams))
        table.update(Settings(key="twitter.preferred.lang", value=twitterConfig.preferredLang))
        table.update(Settings(key="twitter.ignore.retweet", value=twitterConfig.ignoreRetweet))
        table.update(Settings(key='reddit.allow.nsfw', value= redditConfig.allowNsfw))
        table.update(Settings(key='reddit.pull.top', value= redditConfig.pullTop))
        table.update(Settings(key='reddit.pull.hot', value= redditConfig.pullHot))
        table.update(Settings(key='youtube.debug.screnshots', value=youtubeConfig.debugScreenshots))

    def updateDiscordValues(self, values: List[EnvDiscordDetails]) -> None:
        table = self.discordWebHooksTable
        for v in values:
            if v.name == "":
                v.name = DiscordWebHooks().__generateName__(v.server, v.channel)
                
            d = DiscordWebHooks(
                name=v.name, 
                server=v.server, 
                channel=v.channel, 
                url=v.url, 
                fromEnv=True
            )
            table.update(d)
            
            
    def runDatabaseTasks(self) -> None:
        self.updateDiscordValues(values=self.e.discord_values)
        UpdateRSSSource().update(values=self.e.rss_values)
        UpdateYoutubeSource().update(values=self.e.youtube_values)
        UpdateRedditSource().update(values=self.e.reddit_values)
        UpdateTwitchSource().update(values=self.e.twitch_values)
        UpdateTwitterSource().update(values=self.e.twitter_values)
        #UpdateInstagramSource().update(values=self.e.instagram_values)
        UpdatePokemonGoHubSource().update(values=self.e.pogo_values)
        UpdatePhantasyStarOnline2Source().update(values=self.e.pso2_values)
        UpdateFinalFantasyXIVSource("topics", self.e.ffxiv_values.topicsEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("notices", self.e.ffxiv_values.noticesEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("maintenance", self.e.ffxiv_values.maintenanceEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("updates", self.e.ffxiv_values.updateEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("status", self.e.ffxiv_values.statusEnabled).update(values=self.e.ffxiv_values)
        
        self.addStaticIcons()
        self.rebuildCache(
            twitchConfig=self.e.twitch_config, 
            twitterConfig=self.e.twitter_config, 
            redditConfig=self.e.reddit_config,
            youtubeConfig = self.e.youtube_config
        )
