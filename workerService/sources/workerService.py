from workerInfra.domain import LoggerInterface
from workerInfra.models import Articles, DiscordQueue
from workerInfra.domain import SourcesInterface
from workerService.db.tableDiscordQueue import DiscordQueueTable
from workerService import EnvReaderService
from workerService.logger import Logger
from workerService.db import ArticlesTable


class WorkerService():
    """
    This is a generic worker that will contain the source it will monitor.
    """

    def __init__(self, source: SourcesInterface):
        self.logger: LoggerInterface = Logger(__class__)
        self.enabled: bool = False
        self.env = EnvReaderService()
        self.source: SourcesInterface = source

    def __threadInit__(self) -> None:
        """This runs a startup process inside the thread"""
        self.source.__enableSource__()

    def init(self) -> None:
        """
        This is the entry point for the worker.
        Once its turned on it will check the Source for new items.
        """
        self.__threadInit__()
        if self.source.isSourceEnabled is False:
            return None

        self.logger.info(f"{self.source.siteName} Worker has started.")

        try:
            news = self.source.getArticles()
            # Check the DB if it has been posted
            for i in news:
                #self.processArticle(i)
                article = self.__addArticleRecord__(i)
                if article == None:
                    continue

                self.__addDiscordRecord__(article)

        except Exception as e:
            self.logger.warning(f"Failed to collect items from {self.source.siteName}.  Going to attempt again later on. {e}")


    def __addArticleRecord__(self, item: Articles) -> Articles:
        table = ArticlesTable()
        
        res = table.getByUrl(item.url)
        if res.id != '':
            return None
        
        # The article has not been posted, add it
        table.add(item)
        res = table.getByUrl(item.url)
        if res.id == '':
            raise Exception(f"Failed to add the record url={item.url}")

        return res

    def __addDiscordRecord__(self, item: Articles) -> None:
        if self.source.isOutputDiscordEnabled is False:
            return None

        table = DiscordQueueTable()
        dq = DiscordQueue(articleId=item.id)
        res = table.add(dq)
        self.__discordQueueMessage__(item, res)

    def __discordQueueMessage__(self, i: Articles, added: bool) -> None:
        msg: str = ""
        if i.title != "":
            msg = i.title
        else:
            msg = i.description

        if added is True:
            self.logger.info(f'"{msg}" was added to the Discord queue.')
        else:
            self.logger.error(f'"{msg}" was not added to add to the Discord queue.')
