from requests import get, post, delete
from newsbotWorker.infra.models import Sources
from .common import RestSql
from typing import List
from json import loads


class SourcesTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/sources"

    def asdict(self, item: Sources) -> dict:
        return {
            'id': item.id,
            'site': item.site,
            'name': item.name,
            'source': item.source,
            'type': item.type.value,
            'value': item.value,
            'enabled': item.enabled,
            'url': item.url,
            'tags': item.tags,
            'fromEnv': item.fromEnv
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

    def __toApi__(self, item: Sources) -> dict:
        return self.asdict(item)

    def __fromApi__(self, item: dict) -> Sources:
        return self.fromDict(item)

    def __singleFromApi__(self, raw: str) -> Sources:
        d = loads(raw)
        return self.__fromApi__(d)

    def __listFromApi__(self, raw: str) -> List[Sources]:
        d: List[dict] = loads(raw)
        l = list()
        for i in d:
            l.append(self.__fromApi__(i))
        return l

    def __generateBlank__(self) -> Sources:
        b = Sources()
        b.id = ''
        return b

    def getAll(self) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all")
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getAllByName(self, name: str) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all/byName", params={'name':name})
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getAllByType(self, type: str) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all/byType", params={'type':type})
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getAllBySource(self, source: str) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all/bySource", params={'source':source})
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getAllByNameAndType(self, name: str,type: str) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all/byNameAndType", params={'name':name, 'type':type})
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getAllByNameAndSource(self, name: str, source: str) -> List[Sources]:
        raw = get(url=f"{self.uri}/get/all/byNameAndType", params={'name':name, 'source':source})
        return self.convertListResults(statusCode=raw.status_code, text=raw.text)

    def getByNameAndSource(self, name: str, source: str) -> Sources:
        raw = get(url=f"{self.uri}/get/byNameAndSource", params={'name':name, 'source':source})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByName(self, name: str) -> Sources:
        raw = get(url=f"{self.uri}/get/byName", params={'name':name})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getBySource(self, source: str) -> Sources:
        raw = get(url=f"{self.uri}/get/bySource", params={'source':source})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getById(self, id: str) -> Sources:
        raw = get(url=f"{self.uri}/get/byId", params={'id':id})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByNameAndSource(self, name: str, source: str) -> Sources:
        raw = get(url=f"{self.uri}/get/byNameAndSource", params={'name':name, 'source': source})
        return self.convertSingleResult(raw.status_code, raw.text)

    def getByNameSourceType(self,name: str, source: str, type: str) -> Sources:
        raw = get(url=f"{self.uri}/get/byNameSourceType", params={'name':name, 'source':source, 'type':type})
        return self.convertSingleResult(raw.status_code, raw.text)

    def find(self, item: Sources) -> Sources:
        body = self.__toApi__(item)
        res = get(url=f"{self.uri}/find", json=body)
        return self.convertSingleResult(res.status_code, res.text)

    def add(self, item: Sources) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/add", json=body)

    def update(self, item: Sources) -> Sources:
        res = self.find(item)
        if res.id == '':
            self.add(item)
            res = self.find(item)
        else:
            res.name = item.name
            res.source = item.source
            res.type = item.type
            res.value = item.value
            res.enabled = item.enabled
            res.url = item.url
            res.tags = item.tags
            res.fromEnv = item.fromEnv
            self.updateByID(id=res.id, item=item)
        return res

    def updateByID(self, id: str, item: Sources) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/update/byId", json= body, params={'id':id})

    def delete(self, id: str) -> None:
        delete(url=f"{self.uri}/delete/byId", params={'id': id})

