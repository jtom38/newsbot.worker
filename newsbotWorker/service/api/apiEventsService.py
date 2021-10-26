from newsbotWorker.infra.enum import SchedulerTriggerEnum
from newsbotWorker.service.initdb import InitDb
from newsbotWorker.service.scheduler import SchedulerService
from newsbotWorker.infra.models import SchedulerJobModel
from newsbotWorker.service.outputs import DiscordOutputService
from newsbotWorker.service.sources import (
    WorkerService, 
    RedditWorkerService,
    YoutubeWorkerService,
    TwitterWorkerService
)


class ApiEventsService():
    def __init__(self) -> None:
        pass

    def startup(self) -> None:
        print("Running start up tasks")
        #InitDb().runDatabaseTasks()
        ss = SchedulerService()
        ss.addJob(SchedulerJobModel(functionName=WorkerService(RedditWorkerService()).init,trigger=SchedulerTriggerEnum.INTERVAL,interval= True,minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(YoutubeWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(TwitterWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))

        #ss.addJob(SchedulerJobModel(functionName=DiscordOutputService().init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        ss.start()

    def shutdown(self) -> None:
        pass