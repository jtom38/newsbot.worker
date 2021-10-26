from os import stat
from typing import List
from datetime import date, datetime
from newsbotWorker.infra.enum import HealthStatusEnum
from pydantic import BaseModel


class HealthServiceModel(BaseModel):
    name: str 
    status: str
    lastCheckIn: datetime


class HealthModel(BaseModel):
    status: str
    outputs: List[HealthServiceModel]
    sources: List[HealthServiceModel]

