from requests import get, post, delete
from newsbotWorker.infra.models import Articles
from .common import RestSql
from typing import List


class ArticlesTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl = self.__getApiUri__()
        self.uri: str = f"{self.baseUrl}/v1/articles"

    def asdict(self, item: Articles) -> dict:
        d = {
            'id': item.id,
            'sourceId': item.sourceId,
            'tags': item.tags,
            'title': item.title,
            'url': item.url,
            'pubDate': item.pubDate,
            'video': item.video,
            'videoHeight': item.videoHeight,
            'videoWidth': item.videoWidth,
            'thumbnail': item.thumbnail,
            'description': item.description,
            'authorName': item.authorName,
            'authorImage': item.authorImage
        }
        return d

    def fromDict(self, item: Articles) -> Articles:
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

    def __toApi__(self, item: Articles) -> dict:
        return self.asdict(item)

    def __fromApi__(self, item: dict) -> Articles:
        return self.fromDict(item)

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
        try:
            res = get(f"{self.uri}/get/byUrl", params={'url': url})
        except Exception as e:
            print("Failed to get details from the API.")
            
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

