
from requests import Response, get
from bs4 import BeautifulSoup


class ParserBase():
    def getContent(self, uri: str = '') -> Response:
        try:
            headers = self.getHeaders()
            if uri == "":
                return get(self.uri, headers=headers)
            else:
                return get(url=uri, headers=headers)
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(
        self, requestsContent: Response = "", seleniumContent: str = ""
    ) -> BeautifulSoup:
        try:
            if seleniumContent != "":
                return BeautifulSoup(seleniumContent, features="html.parser")
            else:
                return BeautifulSoup(requestsContent.content, features="html.parser")
        except Exception as e:
            self.logger.critical(f"failed to parse data returned from requests. {e}")
