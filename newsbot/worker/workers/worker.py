from newsbot.core.constant import SourceName
from newsbot.core.env import Env
from newsbot.core.logger import ILogger, Logger
from newsbot.core.sql import Articles, ArticlesTable, DiscordQueue, DiscordQueueTable
from newsbot.worker.sources.common import ISources
from time import sleep


class Worker:
    """
    This is a generic worker that will contain the source it will monitor.
    """

    def __init__(self, source: ISources):
        self.logger: ILogger = Logger(__class__)
        self.enabled: bool = False
        self.env = Env()
        self.source: ISources = source
        self.articlesTable = ArticlesTable()
        self.queueTable = DiscordQueueTable()
        pass

    def threadInit(self) -> None:
        """This runs a startup process inside the thread"""
        self.source.__enableSource__()

    def init(self) -> None:
        """
        This is the entry point for the worker.
        Once its turned on it will check the Source for new items.
        """
        self.threadInit()
        if self.source.isSourceEnabled is True:
            self.logger.info(f"{self.source.siteName} Worker has started.")

            while True:
                try:
                    news = self.source.getArticles()
                    # Check the DB if it has been posted
                    for i in news:
                        self.processArticle(i)
                except Exception as e:
                    self.logger.warning(f"Failed to collect items from {self.source.siteName}.  Going to attempt again later on. {e}")

                self.logger.debug(f"{self.source.siteName} Worker is going to sleep.")
                sleep(self.env.threadSleepTimer)

    def processArticle(self, item: Articles) -> None:
        res = self.articlesTable.getByUrl(item.url)
        if res.id != '':
            return None

        # The article has not been posted, add it
        self.articlesTable.add(item)
        res = self.articlesTable.getByUrl(item.url)
        if res.id == '':
            raise Exception(f"Failed to add the record url={item.url}")

        if self.source.isOutputDiscordEnabled is True:
            dq = DiscordQueue().convertFromArticle(res)
            res = self.queueTable.add(dq)
            self.discordQueueMessage(item, res)

    def discordQueueMessage(self, i: Articles, added: bool) -> None:
        msg: str = ""
        if i.title != "":
            msg = i.title
        else:
            msg = i.description

        if added is True:
            self.logger.info(f'"{msg}" was added to the Discord queue.')
        else:
            self.logger.error(f'"{msg}" was not added to add to the Discord queue.')
