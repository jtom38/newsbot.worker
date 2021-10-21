from enum import Enum

class SchedulerTriggerEnum(Enum):
    DATE = 'date'
    INTERVAL = 'interval'
    CRON = 'cron'
    NONE = '0'
