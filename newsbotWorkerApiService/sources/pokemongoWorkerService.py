from newsbotWorkerApiInfra.domain import SourcesInterface
from newsbotWorkerApiInfra.base import SourcesBase
from newsbotWorkerApiInfra.enum import SourcesEnum
from newsbotWorkerApiInfra.models import Articles, Sources
from newsbotWorkerApiInfra.exceptions import UnableToFindContent
from newsbotWorkerApiService.logger import Logger
from typing import List
from requests import Response
from bs4 import BeautifulSoup
import re

class PokemonGoWorkerService(SourcesBase, SourcesInterface):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://pokemongohub.net/rss"
        self.setSiteName(SourcesEnum.POKEMONGO)
        self.authorName: str = "Pokemon Go Hub"
        self.setActiveSource(SourcesEnum.POKEMONGO)
        pass

    def getArticles(self) -> List[Articles]:
        for site in self.__links__:
            self.logger.debug(f"{site.name} - Checking for updates.")

            siteContent: Response = self.getContent()
            if siteContent.status_code != 200:
                raise UnableToFindContent(
                    f"Did not get status code 200.  Got status code {siteContent.status_code}"
                )

            bs: BeautifulSoup = self.getParser(requestsContent=siteContent)

            allArticles: List[Articles] = list()
            try:
                mainLoop = bs.contents[1].contents[1].contents

                for i in mainLoop:
                    if i.name == "item":
                        item: Articles = self.processItem(i)

                        # we are doing the check here to see if we need to fetch the thumbnail.
                        # if we have seen the link already, move on and save on time.
                        seenAlready = self.articlesTable.find(item)
                        if seenAlready.id != '':
                            continue

                        # get thumbnail
                        item.thumbnail = self.getArticleThumbnail(item.url)
                        allArticles.append(item)

                self.logger.debug(f"Pokemon Go Hub - Finished checking.")
            except Exception as e:
                self.logger.error(
                    f"Failed to parse articles from Pokemon Go Hub.  Chances are we have a malformed response. {e}"
                )

        return allArticles

    def processItem(self, item: object) -> Articles:
        a = Articles(
            authorName=self.authorName,
            tags="pokemon go hub, pokemon, go, hub, news",
            sourceId=self.__activeRecord__.id
        )

        for i in item.contents:
            if i.name == "title":
                a.title = i.next
            elif i.name == "link":
                a.url = self.removeHTMLTags(i.next)
            elif i.name == "pubdate":
                #a.pubDate = i.next
                pass
            elif i.name == "category":
                a.tags += f", {i.next.lower()}"
            elif i.name == "description":
                a.description = self.removeHTMLTags(i.next)
            elif i.name == "content:encoded":
                a.content = i.next
        return a

    def removeHTMLTags(self, text: str) -> str:
        tags = ("<p>", "</p>", "<img >", "<h2>")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace("<p>", "")
        text = text.replace("</p>", "\r\n")
        text = text.replace("&#8217;", "'")
        spans = re.finditer("(?<=<span )(.*)(?=>)", text)
        try:
            if len(spans) >= 1:
                print("money")
        except:
            pass

        return text

    def getArticleThumbnail(self, link: str) -> str:
        try:
            #self.uri = link
            r = self.getContent(uri=link)
            bs: BeautifulSoup = BeautifulSoup(r.content, features="html.parser")
            res = bs.find_all("img", class_="entry-thumb")
            return res[0].attrs["src"]
        except Exception as e:
            self.logger.error(f"Failed to pull Pokemon Go Hub thumbnail or {link}. {e}")
