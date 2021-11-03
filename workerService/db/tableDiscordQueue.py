from requests import get, post, delete
from workerInfra.models import DiscordQueue
from .common import RestSql
from typing import List
from json import loads

class DiscordQueueTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/discordqueue"

    def asdict(self, item: DiscordQueue) -> dict:
        return {
            'id': item.id,
            'articleId': item.articleId
        }

    def fromDict(self, item: dict) -> DiscordQueue:
        i = DiscordQueue(
            articleId = item['articleId']
            ,id = item['id']
        )
        return i

    def __toApi__(self, item: DiscordQueue) -> dict:
        return self.asdict(item)

    def __fromApi__(self, item: dict) -> DiscordQueue:
        return self.fromDict(item)

    def __singleFromApi__(self, raw: str) -> DiscordQueue:
        d = loads(raw)
        return self.__fromApi__(d)

    def __listFromApi__(self, raw:str) -> List[DiscordQueue]:
        d: List[dict] = loads(raw)
        l = list()
        for i in d:
            l.append(self.__fromApi__(i))
        return l

    def __generateBlank__(self) -> DiscordQueue:
        return DiscordQueue()

    def getAll(self) -> List[DiscordQueue]:
        raw = get(url=f"{self.uri}/get/all")
        items: List[DiscordQueue] = self.__listFromApi__(raw.text)
        return items


    def getById(self, id: str) -> List[DiscordQueue]:
        raw = get(url=f"{self.uri}/get/byId", params={'id': id})
        item: DiscordQueue = self.__singleFromApi__(raw.text)
        return item

    def add(self, item: DiscordQueue) -> bool:
        body = self.__toApi__(item)
        try:
            post(url=f"{self.uri}/add", json=body)
            return True
        except:
            return False

    def deleteById(self, id: str) -> None:
        delete(url=f"{self.uri}/delete/id", params={'id': id})
