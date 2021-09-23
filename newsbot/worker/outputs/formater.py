
import re
from newsbot.core.constant import SourceName

class DiscordFormat():
    """
    This class is here to convert HTML to Discord formatting.
    """
    
    def convertFromHtml(self, msg: str) -> str:
        msg = msg.replace("<h2>", "**")
        msg = msg.replace("</h2>", "**")
        msg = msg.replace("<h3>", "**")
        msg = msg.replace("</h3>", "**\r\n")
        msg = msg.replace("<strong>", "**")
        msg = msg.replace("</strong>", "**\r\n")
        msg = msg.replace("<ul>", "\r\n")
        msg = msg.replace("</ul>", "")
        msg = msg.replace("</li>", "\r\n")
        msg = msg.replace("<li>", "> ")
        msg = msg.replace("&#8220;", '"')
        msg = msg.replace("&#8221;", '"')
        msg = msg.replace("&#8230;", "...")
        msg = msg.replace("<b>", "**")
        msg = msg.replace("</b>", "**")
        msg = msg.replace("<br>", "\r\n")
        msg = msg.replace("<br/>", "\r\n")
        msg = msg.replace("\xe2\x96\xa0", "*")
        msg = msg.replace("\xa0", "\r\n")
        msg = msg.replace("<p>", "")
        msg = msg.replace("</p>", "\r\n")

        msg = self.replaceLinks(msg)
        return msg

    def replaceLinks(self, msg: str) -> str:
        """
        Find the HTML links and replace them with something discord supports.
        """
        # links = re.findall("(?<=<a )(.*)(?=</a>)", msg)
        msg = msg.replace("'", '"')
        links = re.findall("<a(.*?)a>", msg)
        for l in links:
            hrefs = re.findall('href="(.*?)"', l)
            texts = re.findall(">(.*?)</", l)
            if len(hrefs) >= 1 and len(texts) >= 1:
                discordLink = f"[{texts[0]}]({hrefs[0]})"
                msg = msg.replace(f"<a{l}a>", discordLink)
        return msg

    
    def getEmbedColor(self, sourceType: str, sourceName: str) -> int:
        # Decimal values can be collected from https://www.spycolor.com
        if SourceName.REDDIT.value in sourceType:
            return 16395272
        elif SourceName.YOUTUBE.value  in sourceType:
            return 16449542
        elif SourceName.INSTAGRAM.value in sourceType:
            return 13303930
        elif SourceName.TWITTER.value in sourceType:
            return 1937134
        elif SourceName.FINALFANTASYXIV.value in sourceType:
            return 11809847
        elif SourceName.POKEMONGO.value in sourceType:
            return 2081673
        elif SourceName.PHANTASYSTARONLINE2.value in sourceType:
            return 5557497
        elif SourceName.TWITCH.value in sourceType:
            return 9718783
        elif SourceName.RSS.value in sourceType:
            #self.getRssEmbedColor(sourceName=sourceName)
            return 0
        else:
            return 0