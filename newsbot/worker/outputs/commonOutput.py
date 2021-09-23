from typing import List
from newsbot.core.constant import SourceName
from newsbot.worker.outputs.errors import *
from newsbot.core.sql import *

class CommonOutput():
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
            if source == SourceName.POKEMONGO.value:
                dbHooks = table.getAllBySourceType(sourceType=source)

            elif source == SourceName.PHANTASYSTARONLINE2.value:
                dbHooks = table.getAllBySourceType(sourceType=source)

            elif source == SourceName.FINALFANTASYXIV.value:
                dbHooks = table.getAllBySourceNameAndType(sourceName=name, sourceType=source )
                #dbHooks = table.__filterDupes__(dbHooks)
            
            elif SourceName.TWITTER.value in source:
                dbHooks = table.getAllBySourceNameAndType(sourceType=SourceName.TWITTER.value, sourceName=name)

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

