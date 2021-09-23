from requests import get, post, delete
from newsbot.core.sql.schema import SourceLinks
from typing import List
from json import loads
from os import getenv


class SourceLinksTable():
    def __init__(self):
        # pull from env
        self.baseUrl: str = getenv("NEWSBOT_API_URI")
        self.uri: str = f"{self.baseUrl}/v1/sourcelinks"

    def __toApi__(self, item: SourceLinks) -> dict:
        d = {
            'id': item.id,
            'sourceID': item.sourceID,
            'sourceName': item.sourceName,
            'sourceType': item.sourceType,
            'discordID': item.discordID,
            'discordName': item.discordName,
        }
        return d

    def __fromApi__(self, item: dict) -> SourceLinks:
        a= SourceLinks(
            sourceID=item['sourceID'],
            sourceName=item['sourceName'],
            sourceType=item['sourceType'],
            discordID=item['discordID'],
            discordName=item['discordName'],
        )
        a.id=item['id']
        return a

    def __singleFromApi__(self, raw: str) -> SourceLinks:
        d = loads(raw)
        return self.__fromApi__(d)

    def __listFromApi__(self, raw:str) -> List[SourceLinks]:
        d: List[dict] = loads(raw)
        l = list()
        for i in d:
            l.append(self.__fromApi__(i))
        return l

    def getAll(self) -> List[SourceLinks]:
        raw = get(url=f"{self.uri}/get/all")
        items: List[SourceLinks] = self.__listFromApi__(raw.text)
        return items

    def getBySourceId(self, id: str) -> SourceLinks:
        raw = get(url=f"{self.uri}/get/bySourceId", params={'sourceId': id})
        item = self.__singleFromApi__(raw.text)
        return item

    def getAllBySourceName(self,name:str) -> List[SourceLinks]:
        raw = get(url=f"{self.uri}/get/all/bySourceName", params={'name':name})
        items: List[SourceLinks] = self.__listFromApi__(raw.text)
        return items

    def getAllBySourceType(self,sourceType:str) -> List[SourceLinks]:
        raw = get(url=f"{self.uri}/get/all/bySourceType", params={'sourceType':sourceType})
        items: List[SourceLinks] = self.__listFromApi__(raw.text)
        return items

    # def getAllBySource(self,source:str) -> List[SourceLinks]:
    #    raw = get(url=f"{self.uri}/get/all/bySource", params={'source':source})
    #    items: List[SourceLinks] = self.__listFromApi__(raw.text)
    #    return items

    # def getAllBySourceNameAndSource(self,sourceName:str,source:str) -> List[SourceLinks]:
    #     return NotImplementedError()
    #     raw = get(url=f"{self.uri}/get/all/bySourceNameAndType", 
    #         params={'sourceName':sourceName, 'sourceType':sourceType}
    #     )
    #     if raw.status_code == 404:
    #         l = list()
    #         l.append(SourceLinks())
    #         return l
    #     elif raw.status_code == 200:
    #         if raw.text == '[]':
    #             l = list()
    #             l.append(SourceLinks())
    #             return l
    #         else:
    #             items: List[SourceLinks] = self.__listFromApi__(raw.text)
    #             return items

    def getAllBySourceNameAndType(self,sourceName:str,sourceType:str) -> List[SourceLinks]:
        raw = get(url=f"{self.uri}/get/all/bySourceNameAndType", 
            params={'sourceName':sourceName, 'sourceType':sourceType}
        )
        if raw.status_code == 404:
            l = list()
            l.append(SourceLinks())
            return l
        elif raw.status_code == 200:
            if raw.text == '[]':
                l = list()
                l.append(SourceLinks())
                return l
            else:
                items: List[SourceLinks] = self.__listFromApi__(raw.text)
                return items

    def getBySourceNameAndSourceTypeAndDiscordName(self,sourceName:str,sourceType:str, discordName:str) -> SourceLinks:
        raw = get(url=f"{self.uri}/get/bySourceNameAndSourceTypeAndDiscordName", 
            params={'sourceName':sourceName, 'sourceType':sourceType, 'discordName': discordName}
        )
        if raw.status_code == 404:
            l = list()
            l.append(SourceLinks())
            return l
        elif raw.status_code == 200:
            if raw.text == 'null':
                return SourceLinks()
            else:
                items: SourceLinks = self.__singleFromApi__(raw.text)
                return items

    def getByDiscordId(self,name:str) -> SourceLinks:
        raw = get(url=f"{self.uri}/get/byName", params={'name':name})
        if raw.status_code == 404:
            return SourceLinks()
        elif raw.status_code == 200:
            items: SourceLinks = self.__singleFromApi__(raw.text)
            return items

    def exists(self, item: SourceLinks) -> SourceLinks:
        body = self.__toApi__(item)
        res = get(url=f"{self.uri}/exists", json=body)
        if res.status_code == 404:
            return SourceLinks()
        else:
            i = self.__singleFromApi__(res.text)
            if i.id != '':
                return i
            else:
                return SourceLinks()

    def update(self, item: SourceLinks) -> SourceLinks:
        res = self.exists(item)
        if res.id == "":
            self.add(item)
            res = self.exists(item)
        else:
            res.sourceID = item.sourceID
            res.sourceType = item.sourceType
            res.sourceName = item.sourceName
            res.discordID = item.discordID
            res.discordName = item.discordName
            self.updateById(id=res.id, item=item)
        return res

    def add(self, item: SourceLinks) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/add", json=body)

    def updateById(self, id: str, item: SourceLinks) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/update/byId", json= body, params={'id':id})

    def delete(self, id: str) -> None:
        delete(url=f"{self.uri}/delete/byId", params={'id': id})

