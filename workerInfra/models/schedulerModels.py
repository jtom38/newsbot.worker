from dataclasses import dataclass
from pydantic import BaseModel
from workerInfra.enum import SchedulerTriggerEnum

@dataclass
class SchedulerJobModel():
    functionName: object
    trigger: SchedulerTriggerEnum
    #interval: bool 
    minutes: int = 5
    enabled: bool = True

class SchedulerActveJobsModel(BaseModel):
    name: str
    maxInstances: int
    intervalSeconds: int

