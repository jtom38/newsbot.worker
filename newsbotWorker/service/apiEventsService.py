from newsbotWorker.infrastructure.enum import SchedulerTriggerEnum
from newsbotWorker.service.initdb import InitDb
from newsbotWorker.service.scheduler import SchedulerService
from newsbotWorker.service.demoJobService import DemoJobService
from newsbotWorker.infrastructure.models import SchedulerJobModel
from newsbotWorker.service.sources import WorkerService, RedditWorkerService


class ApiEventsService():
    def __init__(self) -> None:
        pass

    def startup(self) -> None:
        print("Running start up tasks")
        #InitDb().runDatabaseTasks()
        ss = SchedulerService()
        interval= SchedulerTriggerEnum.INTERVAL
        #ss.addJob(SchedulerJobModel(
        #    functionName=DemoJobService().start, 
        #    trigger=interval,
        #    interval=True, 
        #    minutes=1
        #    )
        #)
        ss.addJob(
            SchedulerJobModel(
                functionName=WorkerService(RedditWorkerService()).init,
                trigger=SchedulerTriggerEnum.INTERVAL,
                interval= True,
                minutes=1
            )
        )
        ss.start()

    def shutdown(self) -> None:
        pass