from datetime import date, datetime
import re
from typing import Optional
from newsbot.core.constant import SourceName, SourceType

class Articles():
    id: Optional[str] 
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

    def asdict(self) -> object:
        d = {
            'id': self.id,
            'sourceId': self.sourceId,
            'tags': self.tags,
            'title': self.title,
            'url': self.url,
            'pubDate': self.pubDate,
            'video': self.video,
            'videoHeight': self.videoHeight,
            'videoWidth': self.videoWidth,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'authorName': self.authorName,
            'authorImage': self.authorImage
        }
        return d

    def fromDict(self, item: object) -> object:
        a= Articles(
            sourceId=item['sourceId'],
            tags=item['tags'],
            title=item['title'],
            url=item['url'],
            pubDate=item['pubDate'],
            video=item['video'],
            videoHeight=item['videoHeight'],
            videoWidth=item['videoWidth'],
            thumbnail=item['thumbnail'],
            description=item['description'],
            authorImage=item['authorImage'],
            authorName=item['authorName']
        )
        a.id = item['id']
        return a

class DiscordQueue():
    id: str
    articleId: str

    def __init__(self) -> None:
        self.id = ''
        self.articleId = ''
        pass

    def convertFromArticle(self, item: Articles) -> object:
        i = DiscordQueue()
        i.articleId = item.id
        return i

    def asdict(self) -> dict:
        return {
            'id': self.id,
            'articleId': self.articleId
        }

    def fromDict(self, item: object) -> object:
        i = DiscordQueue()
        i.articleId = item['articleId']
        i.id = item['id']
        return i

class DiscordWebHooks():
    id: Optional[str]
    name: Optional[str]
    key: Optional[str]
    url: Optional[str]
    server: Optional[str]
    channel: Optional[str]
    enabled: bool
    fromEnv: bool

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

class Icons():
    def __init__(self, fileName: str = '', site: str = '') -> None:
        self.id: Optional[str] = ''
        self.filename: Optional[str] = fileName
        self.site: Optional[str]  = site

class Settings():
    def __init__(self, 
        key:str = '', 
        value: str = '',
        options: str = '',
        notes: str = ''
    ) -> None:
        self.id = ''
        self.key = key
        self.value = value
        self.options = options
        self.notes = notes

class SourceLinks():
    def __init__(self, 
        sourceName: SourceName = "", 
        sourceID: str = "", 
        sourceType: str = '',
        discordName: str = '', 
        discordID: str = ""
        ) -> None:
        self.id = ''
        self.sourceID = sourceID
        self.sourceType = sourceType
        self.sourceName = sourceName
        self.discordID = discordID
        self.discordName = discordName

class Sources():
    def __init__(
        self,
        site: str = "",
        name: str = "",
        source: str = "",
        type: str = "",
        value: str = "",
        enabled: bool = True,
        url: str = "",
        tags: str = "",
        fromEnv: bool = False
    ) -> None:
        self.id = ''
        self.site: str = site
        self.name: str = name
        self.source: str = source
        self.type: str = type
        self.value: str = value
        self.enabled: bool = enabled
        self.url: str = url
        self.tags: str = tags
        self.fromEnv: bool = fromEnv

    def asdict(self) -> dict:
        return {
            'id': self.id,
            'site': self.site,
            'name': self.name,
            'source': self.source,
            'type': self.type,
            'value': self.value,
            'enabled': self.enabled,
            'url': self.url,
            'tags': self.tags,
            'fromEnv': self.fromEnv
        }

    def fromDict(self, item: object) -> object:
        a= Sources(
            site= item['site'],
            name=item['name'],
            source=item['source'],
            type=item['type'],
            value=item['value'],
            enabled=item['enabled'],
            url=item['url'],
            tags=item['tags'],
            fromEnv=item['fromEnv']
        )
        a.id=item['id']
        return a