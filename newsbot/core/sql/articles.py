from requests import get, post, delete
from newsbot.core.sql.schema import Articles
from newsbot.core.sql.common import RestSql
from typing import List


class ArticlesTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/articles"

    def __toApi__(self, item: Articles) -> dict:
        return item.asdict()

    def __fromApi__(self, item: dict) -> Articles:
        return Articles().fromDict(item)

    def __generateBlank__(self) -> Articles:
        return Articles()

    def getAll(self) -> List[Articles]:
        raw = get(url=f"{self.uri}/getAll")
        return self.convertListResults(raw.status_code, raw.text)
        # items: List[Articles] = self.__listFromApi__(raw.text)
        # return items

    def getById(self, id: str) -> Articles:
        res = get(url=f"{self.uri}/get/byId", params={'id': id})
        return self.convertSingleResult(res.status_code, res.text)

    def getByUrl(self, url: str) -> Articles:
        res = get(f"{self.uri}/get/byUrl", params={'url': url})
        return self.convertSingleResult(res.status_code, res.text)

    def update(self, item:Articles) -> None:
        res = self.find(item)
        if res.id == '':
            self.add(item)
        else:
            res.siteName = item.siteName
            res.sourceType = item.sourceType
            res.sourceName = item.sourceName
            res.tags = item.tags
            res.title = item.title
            res.url = item.url
            res.pubDate = item.pubDate
            res.video = item.video
            res.videoHeight = item.videoHeight
            res.videoWidth = item.videoWidth
            res.thumbnail = item.thumbnail
            res.description = item.description
            res.authorName = item.authorName
            res.authorImage = item.authorImage

            self.add(res)

    def find(self, item: Articles) -> Articles:
        body = self.__toApi__(item)
        res = get(url=f"{self.uri}/find", json=body)
        return self.convertSingleResult(res.status_code, res.text)

    def add(self, item: Articles) -> None:
        try:
            body = self.__toApi__(item)
            post(url=f"{self.uri}/add", json=body)
        except:
            print("failed to add item to Articles.")

