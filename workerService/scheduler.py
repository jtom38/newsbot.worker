from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from workerInfra.enum.schedulerEnum import SchedulerTriggerEnum
from workerInfra.models import SchedulerJobModel
from workerInfra.models.schedulerModels import SchedulerActveJobsModel
from typing import List


__jobstore__ = {
    'default': MemoryJobStore()
}
__executors__ = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
__job_defaults__ = {
    'coalesce': False,
    'max_instances': 3
}
global __scheduler__
__scheduler__ = BackgroundScheduler(
    jobstores=__jobstore__,
    executors=__executors__,
    job_defaults=__job_defaults__,
)

class SchedulerService():
    def __init__(self) -> None:
        pass

    def start(self) -> None:
        print("Scheduler has started.")
        __scheduler__.start()

    def shutdown(self) -> None:
        print("Scheduler has shutdown.")
        __scheduler__.shutdown()

    def addJob(self, job: SchedulerJobModel) -> None:
        if job.trigger == SchedulerTriggerEnum.INTERVAL:
            __scheduler__.add_job(job.functionName, "interval", minutes=job.minutes,max_instances=1)
        else:
            __scheduler__.add_job(job.functionName)

    def getjobs(self) -> List[SchedulerActveJobsModel]:
        res = __scheduler__.get_jobs()
        l = list()
        for i in res:
            m = SchedulerActveJobsModel(
                name=i.name
                ,maxInstances=i.max_instances
                ,intervalSeconds=i.trigger.interval.seconds
            )
            l.append(m)
        return l
