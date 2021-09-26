from requests import get, post, delete
from newsbot.core.sql.schema import DiscordWebHooks
from newsbot.core.sql.common import RestSql
from typing import List


class DiscordWebHooksTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/discordwebhooks"

    def __generateBlank__(self) -> DiscordWebHooks:
        return DiscordWebHooks()

    def __toApi__(self, item: DiscordWebHooks) -> dict:
        d = {
            'id': item.id,
            'name': item.name,
            'key': item.key,
            'url': item.url,
            'server': item.server,
            'channel': item.channel,
            'enabled': item.enabled,
            'fromEnv': item.fromEnv
        }
        return d

    def __fromApi__(self, item: dict) -> DiscordWebHooks:
        a= DiscordWebHooks(
            name=item['name'], 
            key=item['key'],
            server=item['server'],
            channel=item['channel'],
            url=item['url'],
            fromEnv=item['fromEnv']
        )
        a.id = item['id']
        return a

    def getAll(self) -> List[DiscordWebHooks]:
        raw = get(url=f"{self.uri}/get/all")
        return self.convertListResults(raw.status_code, raw.text)

    def getAllByName(self, name: str) -> List[DiscordWebHooks]:
        raw = get(url=f"{self.uri}/get/all/byName", params={'name': name})
        return self.convertListResults(raw.status_code, raw.text)

    def getById(self, id: str) -> DiscordWebHooks:
        raw = get(url=f"{self.uri}/get/byId", params={"id": id})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByName(self, name: str) -> DiscordWebHooks:
        raw = get(url=f"{self.uri}/get/byName", params={"name": name})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByUrl(self, url: str) -> DiscordWebHooks:
        raw = get(url=f"{self.uri}/get/byUrl", params={"url": url})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByServer(self, server: str) -> DiscordWebHooks:
        raw = get(url=f"{self.uri}/get/byServer", params={"server": server})
        return self.convertSingleResult(raw.status_code, raw.text)

    def find(self, item: DiscordWebHooks) -> DiscordWebHooks:
        body = self.__toApi__(item) 
        res = get(url=f"{self.uri}/find", json=body)
        return self.convertSingleResult(res.status_code, res.text)

    def update(self, item:DiscordWebHooks) -> DiscordWebHooks:
        res = self.find(item)
        if res.id == '':
            self.add(item)
            res = self.find(item)
        else:
            res.name = item.name
            res.key = item.key
            res.url = item.url
            res.server = item.server
            res.channel = item.channel
            res.enabled = item.enabled
            res.fromEnv = item.fromEnv
            self.updateByID(id=res.id, item=res)
        return res

    def add(self, item: DiscordWebHooks) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/add", json=body)

    def updateByID(self, id: str, item: DiscordWebHooks) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/update/byId", json= body, params={'id':id})
