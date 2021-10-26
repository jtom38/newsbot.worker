from fastapi import APIRouter
from typing import List
from newsbotWorker.service.scheduler import SchedulerService
from newsbotWorker.infra.models import SchedulerActveJobsModel

router = APIRouter(
    prefix='/scheduler'
    ,tags=['Scheduler']
)

@router.get('/get/jobs')
def getJobs() -> List[SchedulerActveJobsModel]:
    ss = SchedulerService()
    jobs = ss.getjobs()
    print(jobs)
    return jobs