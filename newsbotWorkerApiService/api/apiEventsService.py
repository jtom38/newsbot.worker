from newsbotWorkerApiInfra.enum import SchedulerTriggerEnum
from newsbotWorkerApiService.initdb import InitDb
from newsbotWorkerApiService.scheduler import SchedulerService
from newsbotWorkerApiInfra.models import SchedulerJobModel
from newsbotWorkerApiService.outputs import DiscordOutputService
from newsbotWorkerApiService.sources import (
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
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(TwitterWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(TwitchWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(PokemonGoWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        #ss.addJob(SchedulerJobModel(functionName=WorkerService(FFXIVWorkerService()).init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))

        ss.addJob(SchedulerJobModel(functionName=DiscordOutputService().init, trigger=SchedulerTriggerEnum.INTERVAL, interval=True, minutes=1))
        ss.start()

    def shutdown(self) -> None:
        pass