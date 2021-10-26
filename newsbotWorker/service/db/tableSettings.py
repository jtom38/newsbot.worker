from requests import get, post, delete
from newsbotWorker.infra.models import Settings
from .common import RestSql
from typing import List
from json import loads


class SettingsTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/settings"

    def __toApi__(self, item: Settings) -> dict:
        d = {
            'id': item.id,
            'key': item.key,
            'value': item.value,
            'options': item.options,
            'notes': item.notes,
        }
        return d

    def __fromApi__(self, item: dict) -> Settings:
        a= Settings(
            key=item['key'],
            value=item['value'],
            options=item['options'],
            notes=item['notes'],
        )
        a.id=item['id']
        return a

    def __singleFromApi__(self, raw: str) -> Settings:
        d = loads(raw)
        return self.__fromApi__(d)

    def __listFromApi__(self, raw:str) -> List[Settings]:
        d: List[dict] = loads(raw)
        l = list()
        for i in d:
            l.append(self.__fromApi__(i))
        return l

    def getAll(self) -> List[Settings]:
        raw = get(url=f"{self.uri}/get/all")
        items: List[Settings] = self.__listFromApi__(raw.text)
        return items

    def getByKey(self,key:str) -> Settings:
        raw = get(url=f"{self.uri}/get/byKey", params={'key':key})
        items: Settings = self.__singleFromApi__(raw.text)
        return items

    def find(self, item:Settings) -> Settings:
        body = self.__toApi__(item)
        res = get(url=f"{self.uri}/find", json=body)
        if res.status_code == 404:
            return Settings()
        else:
            i = self.__singleFromApi__(res.text)
            if i.id != '':
                return i
            else:
                return Settings()

    def update(self, item:Settings) -> None:
        res = self.find(item)
        if res.id == '':
            self.add(item)
        else:
            res.key = item.key
            res.value = item.value
            res.notes = item.notes
            res.options = item.options
            self.updateById(id=res.id, item=res)

    def add(self, item: Settings) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/add", json=body)

    def updateById(self, id: str, item: Settings) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/update/byId", json=body, params={'id': id})

    def delete(self, id: str) -> None:
        delete(url=f"{self.uri}/delete/byId", params={'id': id})

