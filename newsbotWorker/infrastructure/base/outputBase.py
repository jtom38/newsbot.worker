from typing import List
from re import findall
from newsbotWorker.infrastructure.enum import SourcesEnum
from newsbotWorker.infrastructure.exceptions import DiscordWebHookNotFound
from newsbotWorker.service.db import DiscordQueueTable, ArticlesTable, SourcesTable, SourceLinksTable, DiscordWebHooksTable, IconsTable

class ConvertHtml:
    """
    This class is used on outputs to clean up HTML code and replce objects with native formatting.
    """
    def findAllImages(self, text: str) -> List[str]:
        """
        About:
        Returns all the img tags found in the given text.

        Returns:
        List[str]
        """
        imgs = findall("<img (.*?)>", text)
        return imgs

    def replaceImages(self, msg: str, replaceWith: str) -> str:
        """
        About:
        Replaces all img tags found with new text.

        Returns:
        str
        """
        imgs = findall("<img (.*?)>", msg)
        for i in imgs:
            replace = f"<img {i}>"
            msg = msg.replace(replace, replaceWith)
        return msg

class OutputBase():
    """
    This class contains some of the common logic that can be used by other outputs.
    """

    def enableTables(self) -> None:
        self.tableDiscordQueue = DiscordQueueTable()
        self.tableArticles = ArticlesTable()
        self.tableSources = SourcesTable()
        self.tableSourceLinks = SourceLinksTable()
        self.tableDiscordWebHooks = DiscordWebHooksTable()
        self.tableIcons = IconsTable()

    def getHooks(self, source: str, name: str) -> List[str]:
        if name == '':
            self.logger.warning(f"{source} is missing a name!")

        if source == '':
            self.logger.warning(f"A null source name was given!")

        hooks = list()
        table = self.tableSourceLinks
        try:
            if source == SourcesEnum.POKEMONGO.value:
                dbHooks = table.getAllBySourceType(sourceType=source)

            elif source == SourcesEnum.PHANTASYSTARONLINE2.value:
                dbHooks = table.getAllBySourceType(sourceType=source)

            elif source == SourcesEnum.FINALFANTASYXIV.value:
                dbHooks = table.getAllBySourceNameAndType(sourceName=name, sourceType=source )
                #dbHooks = table.__filterDupes__(dbHooks)
            
            elif SourcesEnum.TWITTER.value in source:
                dbHooks = table.getAllBySourceNameAndType(sourceType=SourcesEnum.TWITTER.value, sourceName=name)

            else:
                dbHooks = table.getAllBySourceNameAndType(sourceName=name, sourceType=source)
            
            for hook in dbHooks:
                item = self.tableDiscordWebHooks.getById(hook.discordID)
                if item.url == "":
                    raise Exception("Requested a DiscordWebHook object but the object came back invalid.")

                hooks.append(item.url)
            return hooks
        except DiscordWebHookNotFound as e:
            self.logger.critical(f"Unable to find DiscordWebhook for {source} {name}")

