from datetime import date
from dataclasses import dataclass
from typing import Optional
from workerInfra.enum import SourceTypeEnum

@dataclass
class Articles():
    sourceId: Optional[str]
    tags: Optional[str]
    title: Optional[str]
    url: Optional[str]
    pubDate: Optional[date]
    video: Optional[str]
    videoHeight: Optional[int]
    videoWidth: Optional[int]
    thumbnail: Optional[str]
    description: Optional[str]
    authorName: Optional[str]
    authorImage: Optional[str]
    id: Optional[str] = ''

    def __init__(
        self,
        sourceId: str = '',
        tags: str = "",
        title: str = "",
        url: str = "",
        pubDate: str = "",
        video: str = "",
        videoHeight: int = 0,
        videoWidth: int = 0,
        thumbnail: str = "",
        description: str = "",
        authorName: str = "",
        authorImage: str = "",
    ) -> None:
        self.id = ''
        self.sourceId = sourceId
        self.tags = tags
        self.title = title
        self.url = url
        if pubDate == '':
            # add today's date
            dt = date.today()
            today = f"{dt.year}-{dt.month}-{dt.day}"
            self.pubDate = today
        else: self.pubDate = pubDate
        self.video = video
        self.videoHeight = videoHeight
        self.videoWidth = videoWidth
        self.thumbnail = thumbnail
        self.description = description
        self.authorName = authorName
        self.authorImage = authorImage

    def setPubDate(self, value: str = '') -> None:
        if value == '':
            # add today's date
            dt = date.today()
            today = f"{dt.year}-{dt.month}-{dt.day}"
            self.pubDate = today
        else: self.pubDate = value


@dataclass
class DiscordQueue():
    articleId: str
    id: str = ''

    @staticmethod
    def convertFromArticle(item: Articles) -> object:
        i = DiscordQueue()
        i.articleId = item.id
        return i

class DiscordWebHooks():
    name: Optional[str]
    key: Optional[str]
    url: Optional[str]
    server: Optional[str]
    channel: Optional[str]
    enabled: bool
    fromEnv: bool
    id: Optional[str] = ''

    def __init__(
        self,
        name: str = "",
        key: str = "",
        server: str = "",
        channel: str = "",
        url: str = "",
        fromEnv: bool = False
    ) -> None:
        self.name = name
        self.id = ''
        self.server = server
        self.channel = channel
        if name == "":  
            self.name = self.__generateName__(server, channel)
        else: 
            self.name = name
        self.key = key
        self.url = url
        self.enabled = True
        self.fromEnv: bool = fromEnv

    def __generateName__(self, server: str, channel: str) -> str:
        return f"{server} - {channel}"

@dataclass
class Icons():
    filename: str
    site: str
    id: str = ''


@dataclass
class Settings():
    key: str = ''
    value: str = ''
    options: str = ''
    notes: str = ''
    id: Optional[str] = ''

    
@dataclass
class SourceLinks():
    id: Optional[str] = ''
    sourceID: str = ''
    sourceName: str = ''
    sourceType: str = ''
    discordName: str = ''
    discordID: str =''


@dataclass
class Sources():
    id: Optional[str] = ''
    site: str = ''
    name: str = ''
    source: str = ''
    enabled: bool = False
    url: str = ''
    tags: str = ''
    fromEnv: bool = False
    type: SourceTypeEnum = SourceTypeEnum.INVALID
    value: str = ''
    
