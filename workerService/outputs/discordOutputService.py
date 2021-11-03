from typing import List
import re
from time import sleep
from workerInfra.enum import SourcesEnum
from workerInfra.models import Articles, Sources, SourceLinks, DiscordQueue, DiscordWebHooks
from workerInfra.domain import OutputInterface, OutputFormatterInterface
from workerInfra.base import OutputBase
from workerInfra.exceptions import DiscordWebHookNotFound
from workerInfra.base import ConvertHtml
from workerService import Logger
from workerService.logger import Logger
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response


class DiscordFormatter(ConvertHtml, OutputFormatterInterface):
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


class DiscordOutputService(OutputInterface, OutputBase, DiscordFormatter):
    def __init__(self) -> None:
        self.enableTables()
        self.logger = Logger(__class__)
        self.tempMessage: DiscordWebhook = DiscordWebhook("placeholder")
        self.article: Articles
        self.source: Sources
        pass

    def init(self) -> None:
        try:
            self.logger.debug("Checking DiscordQueue for objects.")
            queue = self.tableDiscordQueue.getAll()
            for i in queue:
                self.article = self.tableArticles.getById(i.articleId)

                if self.article.title == '' and self.article.url == '':
                    raise Exception("Queue item did not have a valid ArticleId")

                self.source = self.tableSources.getById(self.article.sourceId)
                if self.source.source == '':
                    raise Exception("Source requested from the API did not contain a valid Sources.Source")

                if self.article.title != "":
                    self.logger.info(f"Discord - Sending article '{self.article.title}'")
                else:
                    self.logger.info(f"Discord - Sending article '{self.article.description}'")

                self.buildMessage(self.article, self.source)
                resp = self.sendMessage()
                safeToRemove = self.isSafeToRemove(resp)
                if safeToRemove == True:
                    self.tableDiscordQueue.deleteById(i.id)

                self.webhooks.clear()
                sleep(15)
            self.logger.debug("Local queue is now empty.  Service is exiting.")
        except Exception as e:
            self.logger.error(
                f"Failed to post a message. {self.article.title}. Status_code: {resp[0].status_code}. OK: {resp[0].ok}. error {e}"
            )

    def buildMessage(self, article: Articles, source: Sources) -> None:
        # reset the stored message
        self.tempMessage = DiscordWebhook("placeholder")

        # Extract the webhooks that relate to this site
        webhooks: List[str] = self.getHooks(source=source.source, name=source.name)
        self.webhooks = webhooks

        # Make a new webhook with the hooks that relate to this site
        hook: DiscordWebhook = DiscordWebhook(webhooks)

        title = article.title
        if len(title) >= 128:
            title = f"{title[0:128]}..."

        # Make a new Embed object
        embed: DiscordEmbed = DiscordEmbed(title=title)  # , url=article.link)
        try:
            authorIcon = self.getAuthorIcon(
                icon=article.authorImage,
                name=source.name, 
                type=source.type,
                source=source.source
                )

            embed.set_author(name=article.authorName, url=None, icon_url=authorIcon)
        except:
            pass

        # Discord Embed Description can only contain 2048 characters
        ch = ConvertHtml()
        if article.description != "":
            description: str = str(article.description)
            description = self.convertFromHtml(description)
            description = ch.replaceImages(description, "")
            descriptionCount = len(description)
            if descriptionCount >= 2048:
                description = description[0:2040]
                description = f"{description}..."
            embed.description = description

        # Figure out if we have video based content
        if article.video != "":
            embed.description = "View the video online!"
            embed.set_video(
                url=article.video, height=article.videoHeight, width=article.videoWidth
            )

        try:
            if article.thumbnail != "":
                if " " in article.thumbnail:
                    s = article.thumbnail.split(" ")
                    embed.set_image(url=s[0])
                else:
                    embed.set_image(url=article.thumbnail)
        except Exception as e:
            self.logger.warning(
                f"Failed to attach a thumbnail. \r\n {e}\r\n thumbnails: {article.thumbnail}"
            )

        # add the link to the embed
        embed.add_embed_field(name="Link:", value=article.url)

        # Build our footer message
        footer = self.buildFooter(source= source.source, name=source.name, _type=source.type)
        footerIcon = self.getFooterIcon(siteName=source.name, sourceType=source.source)
        embed.set_footer(icon_url=footerIcon, text=footer)

        embed.set_color(color=self.getEmbedColor(sourceType=source.source, sourceName=source.name))

        hook.add_embed(embed)
        self.tempMessage = hook

    def sendMessage(self) -> List[Response]:
        try:
            res = self.convertToList(self.tempMessage.execute())
        except Exception as e:
            self.logger.critical(
                f"Failed to send to Discord.  Check to ensure the webhook is correct. Error: {e}"
            )
        return res

    def convertToList(self, r: Response) -> List[Response]:
        hooks: int = len(self.webhooks)
        # Chcekcing to see if we returned a single response or multiple.
        if hooks == 1:
            response = list()
            response.append(r)
        else:
            response = r

        return response

    def isSafeToRemove(self, resp: List[Response]) -> bool:
        safeToRemove: bool = True
        for r in resp:
            if r.status_code == 204:
                pass
            elif r.status_code == 200:
                pass
            else:
                self.logger.error("Found a invalid response code.  Expected 204.  Check the webhooks to make sure they are correct.")
                safeToRemove = False

        return safeToRemove

    def getAuthorIcon(self, icon: str, name: str, type: str, source: str) -> str:
        table = self.tableIcons
        if icon != "":
            return icon
        
        # Pull the default icon
        res = table.getBySite(f"Default {source}")
        if res.id != '':
            return res.filename

        try:
            if (
                type == SourcesEnum.FINALFANTASYXIV.value
                or type == SourcesEnum.PHANTASYSTARONLINE2.value
                or type == SourcesEnum.POKEMONGO.value
            ):
                res = table.getBySite(site=f"Default {type}")

            elif source == SourcesEnum.RSS.value:
                res = table.getBySite(site=name)

            return res.filename

        except Exception as e:
            self.logger.error(f"Failed to find the author icon for type:{type} name:{name}")

    def buildFooter(self, source: str, name: str, _type: str = '') -> str:
        footer = ""
        end: str = "Brought to you by NewsBot"

        if SourcesEnum.REDDIT.value in source.lower():
            footer = f"/r/{name} on Reddit - {end}"

        elif SourcesEnum.YOUTUBE.value in source:
            footer = f"{name} on YouTube - {end}"

        elif SourcesEnum.TWITTER .value in source:
            if _type == '':
                raise Exception(f"Expected to find a type for {source}.{name}")
            elif _type == 'user':
                footer = f"@{name} on Twitter - {end}"
            elif _type == "tag":
                footer = f"#{name} on Twitter - {end}"

        elif SourcesEnum.INSTAGRAM.value in source:
            s = source.split(" ")
            if s[1] == "tag":
                footer = f"#{s[2]} - {end}"
            elif s[1] == "user":
                footer = f"{s[2]} - {end}"

        #elif SourceName.RSS.value in source:
            #footer = f"{name} - {end}"

        else:
            footer = end

        return footer

    def getFooterIcon(self, siteName: str, sourceType: str) -> str:
        # A footer icon should always be the default icon.
        table = self.tableIcons
        if sourceType == SourcesEnum.RSS.value:
            res = table.getBySite(site=siteName)
        else:
            res = table.getBySite(site=f"Default {sourceType}")

        if res.filename == "":
            self.logger.error(f"Unable to find the default icon for '{sourceType}'.")

        return res.filename

    def getEmbedColor(self, sourceType: str, sourceName: str) -> int:
        # Decimal values can be collected from https://www.spycolor.com
        if SourcesEnum.REDDIT.value in sourceType:
            return 16395272
        elif SourcesEnum.YOUTUBE.value  in sourceType:
            return 16449542
        elif SourcesEnum.INSTAGRAM.value in sourceType:
            return 13303930
        elif SourcesEnum.TWITTER.value in sourceType:
            return 1937134
        elif SourcesEnum.FINALFANTASYXIV.value in sourceType:
            return 11809847
        elif SourcesEnum.POKEMONGO.value in sourceType:
            return 2081673
        elif SourcesEnum.PHANTASYSTARONLINE2.value in sourceType:
            return 5557497
        elif SourcesEnum.TWITCH.value in sourceType:
            return 9718783
        elif SourcesEnum.RSS.value in sourceType:
            #self.getRssEmbedColor(sourceName=sourceName)
            return 0
        else:
            return 0

