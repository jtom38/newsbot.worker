from typing import List
from workerInfra.domain import LoggerInterface
from workerService.logger import BasicLoggerService
from requests import get, Response
from bs4 import BeautifulSoup


class RequestContent:
    """
    This is a common class that will request site information.
    This class will make use of the Requests and BeautifulSoup librarys.

    Examples:
    RequestContent(url='www').
    RequestContent().setUrl("www").
    """
    __url__: str
    __soup__: BeautifulSoup
    _logger: LoggerInterface

    def __init__(self, url: str = "") -> None:
        self.__url__ = url
        self._logger = BasicLoggerService()
        self.__soup__ = None

    def getUrl(self) -> str:
        if self.__url__ != '':
            return self.__url__
        else:
            raise ValueError("URL is missing from object.")

    def setUrl(self, url: str) -> None:
        """
        If you want to parse a URL, set the value here.
        """
        # self.url = url
        self.__url__ = url

    def setSoup(self, soup: BeautifulSoup) -> None:
        """
        If the source has already been parsed elsewhere, pass the BeautifulSoup object here.
        """
        self.__soup__ = soup

    def __getHeaders__(self) -> dict:
        # return {"User-Agent": "NewsBot - Automated News Delivery"}
        return {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/91.3"}

    def __getSource__(self) -> str:
        try:
            res: Response = get(self.getUrl(), headers=self.__getHeaders__())
            if res.ok is True:
                self.__response__: Response = res
                return res.text
            else:
                self._logger.error(
                    f"Attempted to get data from '{self.getUrl()}' but did not get any data.  StatusCode={res.status_code}"
                )
                return ""
        except Exception as e:
            self._logger.critical(
                f"Failed to get data from '{self.getUrl()}' but resulted in an error. {e} "
            )

    def __getSoup__(self) -> BeautifulSoup:
        try:
            soup = BeautifulSoup(self.__source__, features="html.parser")
            return soup
        except Exception as e:
            self._logger.error(e)
            return BeautifulSoup()

    def getPageDetails(self) -> None:
        """
        This pulls the source code and converts it into a BeautifulSoup object.
        """
        if self.getUrl() == "":
            self._logger.error(
                "Was requested to pull data from a site, but no URL was passed."
            )
        else:
            self.__source__ = self.__getSource__()

        try:
            if self.__soup__ is None:
                self.__soup__ = self.__getSoup__()
            else:
                pass
        except Exception as e:
            self._logger.warning(e)
            self.__soup__ = self.__getSoup__()

        pass

    def findSingle(self, name: str = "", attrKey: str = "", attrValue: str = "") -> BeautifulSoup:
        if attrKey != "":
            attrs = {attrKey: attrValue}
            res = self.__soup__.find(name=name, attrs=attrs)
            return res
        else:
            return self.__soup__.find(name=name)

    def findMany(self, name: str = "", attrKey: str = "", attrValue: str = "") -> List[BeautifulSoup]:
        if attrKey != "":
            return self.__soup__.find_all(name=name, attrs={attrKey: attrValue})
        else:
            return self.__soup__.find_all(name=name)

    def findFeedLink(self) -> dict:
        atom = self.findSingle(
            name="link", attrKey="type", attrValue="application/atom+xml"
        )
        rss = self.findSingle(
            name="link", attrKey="type", attrValue="application/rss+xml"
        )
        json = self.findSingle(
            name="link", attrKey="type", attrValue="application/json"
        )

        if atom is not None:
            return self.__buildFeedDict__("atom", atom.attrs["href"])
        elif rss is not None:
            return self.__buildFeedDict__("rss", rss.attrs["href"])
        elif json is not None:
            return self.__buildFeedDict__("json", json.attrs["href"])
        else:
            return self.__buildFeedDict__("none", None)

    def __buildFeedDict__(self, type: str, content: str) -> dict:
        return {"type": type, "content": content}

    def findSiteIcon(self, siteUrl: str) -> str:
        """
        This will go and attempt to extract the 'apple-touch-icon' from the header.

        return: str
        """
        # if a site url contains the / lets remove it
        if siteUrl.endswith("/") is True:
            siteUrl = siteUrl.strip("/")

        bestSize: int = -1
        icons = self.findMany(name="link", attrKey="rel", attrValue="apple-touch-icon")
        # look though all the icons given, find the largest one.
        for icon in icons:
            size: int = int(icon.attrs["sizes"].split("x")[0])
            if size > bestSize:
                bestSize = size

        # take what we found as the largest icon and store it.
        for icon in icons:
            size: int = int(icon.attrs["sizes"].split("x")[0])
            if size == bestSize:
                href = icon.attrs["href"]
                if "http" in href or "https" in href:
                    return href
                else:
                    return f"{siteUrl}{href}"
        return ""

    def findArticleThumbnail(self) -> str:
        """
        This is best used on articles, not on root the main site page.
        It will go and check the page for defined thumbnails and return the first one it finds, if any.

        return: str
        """
        meta = (
            {"name": "meta", "attrKey": "property", "attrValue": "og:image"},
            {"name": "meta", "attrKey": "name", "attrValue": "twitter:image:src"},
        )

        for i in meta:
            try:
                item = self.findSingle(
                    name=i["name"], attrKey=i["attrKey"], attrValue=i["attrValue"]
                )
                if item.attrs["content"] != "":
                    thumb = item.attrs["content"]
                    return thumb
            except Exception as e:
                self._logger.warning(e)
                pass
        return ""

    def findArticleDescription(self) -> str:
        lookups = (
            {"name": "div", "key": "class", "value": "entry-content e-content"},
            {"name": "div", "key": "class", "value": "engadget-post-contents"},
            {"name": "div", "key": "class", "value": "article-content post-page"},
        )

        for lookup in lookups:
            content = self.findSingle(
                name=lookup["name"], attrKey=lookup["key"], attrValue=lookup["value"]
            )
            if content.text != "":
                return content.text


class RequestSiteContent(RequestContent):
    def findFeedLink(self, siteUrl: str) -> dict:
        atom = self.findSingle(
            name="link", attrKey="type", attrValue="application/atom+xml"
        )
        rss = self.findSingle(
            name="link", attrKey="type", attrValue="application/rss+xml"
        )
        json = self.findSingle(
            name="link", attrKey="type", attrValue="application/json"
        )

        if atom is not None:
            href = self.__cleanUrl__(atom.attrs["href"], siteUrl)
            return self.__buildFeedDict__("atom", href)
        elif rss is not None:
            href = self.__cleanUrl__(rss.attrs["href"], siteUrl)
            return self.__buildFeedDict__("rss", href)
        elif json is not None:
            href = self.__cleanUrl__(json.attrs["href"], siteUrl)
            return self.__buildFeedDict__("json", href)
        elif "feedburner.com" in siteUrl:
            return self.__buildFeedDict__("feedburner", siteUrl)
        else:
            return self.__buildFeedDict__("none", None)

    def __cleanUrl__(self, href: str, siteUrl: str) -> str:
        if href.startswith("//") is True:
            href = href.replace("//", "")

        if "http://" in href or "https://" in href:
            return href

        if "http://" not in href or "https://" not in href:
            return f"{siteUrl}{href}"

        elif "http://" in siteUrl:
            return f"http://{href}"

        elif "https://" in siteUrl:
            return f"https://{href}"

    def __buildFeedDict__(self, type: str, content: str) -> dict:
        return {"type": type, "content": content}

    def findSiteIcon(self, siteUrl: str) -> str:
        """
        This will go and attempt to extract the 'apple-touch-icon' from the header.

        return: str
        """
        # if a site url contains the / lets remove it
        if siteUrl.endswith("/") is True:
            siteUrl = siteUrl.strip("/")

        href = ""
        appleIcon = self.__findAppleIcons__(siteUrl=siteUrl)
        if appleIcon != "":
            href = appleIcon

        if href == "" and appleIcon == "":
            genericIcon = self.__findGenericIcons__(siteUrl=siteUrl)
            if genericIcon != "":
                href = genericIcon

        if "http" in href or "https" in href:
            return href
        elif href == "":
            return href
        else:
            return f"{siteUrl}{href}"

    def __findAppleIcons__(self, siteUrl: str) -> str:
        bestSize: int = -1
        href: str = ""
        icons = self.findMany(name="link", attrKey="rel", attrValue="apple-touch-icon")
        if len(icons) >= 2:
            try:
                # look though all the icons given, find the largest one.
                for icon in icons:
                    try:
                        size: int = int(icon.attrs["sizes"].split("x")[0])
                        if size > bestSize:
                            bestSize = size
                    except Exception as e:
                        self._logger.warning(
                            f"'{siteUrl}' did not have sizes present on the site icon.  Not the standard use of the apple-touch-icon. {e}"
                        )
                        pass

                # take what we found as the largest icon and store it.
                for icon in icons:
                    size: int = int(icon.attrs["sizes"].split("x")[0])
                    if size == bestSize:
                        href = icon.attrs["href"]
            except Exception as e:
                self._logger.warning(f"Failed to find the size of the siteIcon. {e}")
        elif len(icons) == 1:
            href = icons[0].attrs["href"]
        else:
            href = ""

        return href

    def __findGenericIcons__(self, siteUrl: str) -> str:
        # This logic was built from www.omgubuntu.co.uk's logic with how they have icons structured.
        largest: dict = {"size": 0, "url": ""}
        try:
            icons = self.findMany(name="link", attrKey="type", attrValue="image/png")
        except Exception as e:
            self._logger.warning(f"Failed to find generic site icon links. {e}")
            return ""

        try:
            for icon in icons:
                t = int(icon.attrs["sizes"].split("x")[0])
                if t >= largest["size"]:
                    largest["size"] = t
                    largest["url"] = icon.attrs["href"]
        except Exception as e:
            self._logger.warning(f"Failed to parse the generic site icon size. {e}")
            return ""

        return largest["url"]


class RequestArticleContent(RequestContent):
    def findArticleThumbnail(self) -> str:
        """
        This is best used on articles, not on root the main site page.
        It will go and check the page for defined thumbnails and return the first one it finds, if any.

        return: str
        """
        meta = (
            {"name": "meta", "attrKey": "property", "attrValue": "og:image"},
            {"name": "meta", "attrKey": "name", "attrValue": "twitter:image:src"},
        )

        for i in meta:
            try:
                item = self.findSingle(
                    name=i["name"], attrKey=i["attrKey"], attrValue=i["attrValue"]
                )
                if item.attrs["content"] != "":
                    thumb = item.attrs["content"]
                    return thumb
            except Exception as e:
                self._logger.warning(e)
                pass
        return ""

    def findArticleDescription(self) -> str:
        lookups = (
            {
                "name": "div",
                "key": "class",
                "value": "entry-content e-content",
            },  # HowToGeek
            {
                "name": "div",
                "key": "class",
                "value": "engadget-post-contents",
            },  # Engadget
            {
                "name": "div",
                "key": "class",
                "value": "article-content post-page",
            },  # ArsTechnica
        )

        for lookup in lookups:
            try:
                content = self.findSingle(
                    name=lookup["name"], attrKey=lookup["key"], attrValue=lookup["value"]
                )
                if content.text != "":
                    text = ""
                    # Look for just p blocks to avoid ads and junk we dont care about
                    pBlocks = self.findMany(name="p")
                    if len(pBlocks) >= 1:
                        for p in pBlocks:
                            text += f"{p} \r\n"
                    return content.text
            except Exception as e:
                self._logger.warning(e)
                pass
        return ""
