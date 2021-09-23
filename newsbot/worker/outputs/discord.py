from typing import List
import re
from time import sleep
from newsbot.core.constant import SourceName
from newsbot.core.env import Env
from newsbot.core.logger import Logger
from newsbot.core.sql import *
from newsbot.worker.common.convertHtml import ConvertHtml
from newsbot.worker.outputs.ioutputs import IOutputs
from newsbot.worker.outputs.commonOutput import CommonOutput
from newsbot.worker.outputs.errors import DiscordWebHookNotFound
from newsbot.worker.outputs.formater import DiscordFormat
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response

class Discord(IOutputs, CommonOutput, DiscordFormat):
    def __init__(self) -> None:
        self.enableTables()
        self.logger = Logger(__class__)
        self.tempMessage: DiscordWebhook = DiscordWebhook("placeholder")
        self.env = Env()
        self.article: Articles = Articles()
        self.source: Sources = Sources()
        pass

    def enableThread(self) -> None:
        while True:
            # Tell the database to give us the queue on the table.
            try:
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
                    self.threadWait()

                # Once the loop is over, sleep for 5 minutes before checking the table again
                self.logger.debug(f"Local queue is now empty.  Waiting {self.env.discordTableCheckSeconds} seconds before next check")
                sleep(self.env.discordTableCheckSeconds)
            except Exception as e:
                self.logger.error(
                    f"Failed to post a message. {self.article.title}. Status_code: {resp[0].status_code}. OK: {resp[0].ok}. error {e}"
                )

            self.threadWait()

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

    def threadWait(self) -> None:
        sleep(self.env.discord_delay_seconds)

    def replaceImages(self, msg: str) -> str:
        imgs = re.findall("<img (.*?)>", msg)
        for i in imgs:
            # Removing the images for now.
            # src = re.findall('src=(.*?)">', i)
            replace = f"<img {i}>"
            msg = msg.replace(replace, "")
        return msg

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
                type == SourceName.FINALFANTASYXIV.value
                or type == SourceName.PHANTASYSTARONLINE2.value
                or type == SourceName.POKEMONGO.value
            ):
                res = table.getBySite(site=f"Default {type}")

            elif source == SourceName.RSS.value:
                res = table.getBySite(site=name)

            return res.filename

        except Exception as e:
            self.logger.error(f"Failed to find the author icon for type:{type} name:{name}")

    def buildFooter(self, source: str, name: str, _type: str = '') -> str:
        footer = ""
        end: str = "Brought to you by NewsBot"

        if SourceName.REDDIT.value in source.lower():
            footer = f"/r/{name} on Reddit - {end}"

        elif SourceName.YOUTUBE.value in source:
            footer = f"{name} on YouTube - {end}"

        elif SourceName.TWITTER .value in source:
            if _type == '':
                raise Exception(f"Expected to find a type for {source}.{name}")
            elif _type == 'user':
                footer = f"@{name} on Twitter - {end}"
            elif _type == "tag":
                footer = f"#{name} on Twitter - {end}"

        elif SourceName.INSTAGRAM.value in source:
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
        if sourceType == SourceName.RSS.value:
            res = table.getBySite(site=siteName)
        else:
            res = table.getBySite(site=f"Default {sourceType}")

        if res.filename == "":
            self.logger.error(f"Unable to find the default icon for '{sourceType}'.")

        return res.filename

