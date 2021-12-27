from workerInfra.domain import RssHelperInterface


class Engadget(RssHelperInterface):
    def getArticleContent(self) -> str:
        content = self.soup.find(name="div", attrs={"id": "engadget-post-contents"})
        return content.text


class ArsTechnica(RssHelperInterface):
    def getArticleContent(self) -> str:
        content = self.soup.find(
            name="div",
            attrs={"class": "article-content post-page"}
        )
        p = content.find_all(name="p")
        body = ""
        for i in p:
            body += i.text + "\r\n"
        return body


class HowToGeek(RssHelperInterface):
    def getArticleContent(self) -> str:
        pass
