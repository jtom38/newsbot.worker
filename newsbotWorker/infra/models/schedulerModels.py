from dataclasses import dataclass
from pydantic import BaseModel
from newsbotWorker.infra.enum import SchedulerTriggerEnum

@dataclass
class SchedulerJobModel():
    functionName: object
    trigger: SchedulerTriggerEnum
    interval: bool
    minutes: int

class SchedulerActveJobsModel(BaseModel):
    name: str
    maxInstances: int
    intervalSeconds: int

