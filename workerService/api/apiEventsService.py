from workerInfra.enum import SchedulerTriggerEnum
from workerService.initdb import InitDb
from workerService.scheduler import SchedulerService
from workerInfra.models import SchedulerJobModel
from workerService.outputs import DiscordOutputService
from workerService.sources import (
    WorkerService, 
    RedditWorkerService,
    YoutubeWorkerService,
    TwitterWorkerService,
    TwitchWorkerService,
    PokemonGoWorkerService,
    FFXIVWorkerService
)


class ApiEventsService():
    def __init__(self) -> None:
        pass

    def startup(self) -> None:
        print("Running start up tasks")
        InitDb().runDatabaseTasks()
        ss = SchedulerService()
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(RedditWorkerService()).init,trigger=SchedulerTriggerEnum.INTERVAL,interval= True,minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(YoutubeWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        ss.addJob(SchedulerJobModel(functionName=WorkerService(YoutubeWorkerService()).init, trigger=SchedulerTriggerEnum.NONE ))

        #ss.addJob(SchedulerJobModel(functionName=WorkerService(TwitterWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(TwitchWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(PokemonGoWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(FFXIVWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))

        ss.addJob(SchedulerJobModel(functionName=DiscordOutputService().init, trigger=SchedulerTriggerEnum.INTERVAL, minutes=3))
        ss.start()

    def shutdown(self) -> None:
        pass