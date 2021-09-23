from requests import get, post, delete
from newsbot.core.sql.schema import Icons
from newsbot.core.sql.common import RestSql
from typing import List
from os import getenv


class IconsTable(RestSql):
    def __init__(self):
        # pull from env
        self.baseUrl: str = getenv("NEWSBOT_API_URI")
        self.uri: str = f"{self.baseUrl}/v1/icons"

    def __toApi__(self, item: Icons) -> dict:
        d = {
            'id': item.id,
            'filename': item.filename,
            'site': item.site
        }
        return d

    def __fromApi__(self, item: dict) -> Icons:
        a= Icons(
            fileName=item['filename'],
            site=item['site']
        )
        a.id=item['id']
        return a

    def __generateBlank__(self) -> Icons:
        return Icons()

    def getAll(self) -> List[Icons]:
        raw = get(url=f"{self.uri}/get/all")
        return self.convertListResults(raw.status_code, raw.text)
        # items: List[Icons] = self.__listFromApi__(raw.text)
        # return items

    def getBySite(self, site: str) -> Icons:
        raw = get(url=f"{self.uri}/get/bySite", params={"site": site})
        return self.convertSingleResult(raw.status_code, raw.text)
        # items: List[Icons] = self.__singleFromApi__(raw.text)
        # return items

    def find(self, item:Icons) -> Icons:
        body = self.__toApi__(item)
        res = get(url=f"{self.uri}/find", json=body)
        return self.convertSingleResult(res.status_code, res.text)
        # if res.status_code == 404:
        #     return Icons()
        # else:
        #    i = self.__singleFromApi__(res.text)
        #    if i.id != '':
        #        return i
        #    else:
        #        return Icons()

    def update(self, item:Icons) -> None:
        res = self.find(item)
        if res.id == '':
            self.add(item)
        else:
            res.filename = item.filename
            res.site = item.site
            self.updateById(id=res.id, item=res)
            # self.add(res)

    def add(self, item: Icons) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/add", json=body)

    def updateById(self, id: str, item: Icons) -> None:
        body = self.__toApi__(item)
        post(url=f"{self.uri}/update/byId", json=body, params={'id': id})

    def delete(self, link: str) -> None:
        delete(url=f"{self.uri}/delete/url", params={'url': link})